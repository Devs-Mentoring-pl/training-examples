-- =============================================================================
-- Szkolenie 2: SQL w Snowflake
-- =============================================================================
-- Wymaga wcześniejszego uruchomienia 01_setup.sql
-- =============================================================================

USE ROLE sysadmin;
USE WAREHOUSE learn_wh;
USE DATABASE shop_db;
USE SCHEMA raw;

-- -----------------------------------------------------------------------------
-- 1. Deduplikacja wzorcem QUALIFY
-- -----------------------------------------------------------------------------

-- Sprawdzenie duplikatów klucza (Snowflake nie egzekwuje PRIMARY KEY!)
SELECT order_id, COUNT(*) AS cnt
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;

-- Odduplikowanie – zostawiamy najnowszy wiersz dla każdego klucza
CREATE OR REPLACE TRANSIENT TABLE staging.orders_clean AS
SELECT order_id, customer_id, order_date, status, total_amount
FROM orders
QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY order_date DESC) = 1;

-- -----------------------------------------------------------------------------
-- 2. Funkcje okna – top N w grupie
-- -----------------------------------------------------------------------------

-- Trzy najdroższe produkty w każdej kategorii
SELECT
    category,
    name,
    price,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) AS rank_in_category
FROM products
QUALIFY rank_in_category <= 3
ORDER BY category, rank_in_category;

-- Ranking klientów z udziałem w przychodzie kraju
WITH customer_spend AS (
    SELECT
        c.customer_id,
        c.email,
        c.country_code,
        SUM(o.total_amount) AS total_spent
    FROM customers c
    JOIN orders o ON o.customer_id = c.customer_id
    WHERE o.status <> 'CANCELLED'
    GROUP BY 1, 2, 3
)
SELECT
    country_code,
    email,
    ROUND(total_spent, 2) AS total_spent,
    ROW_NUMBER() OVER (PARTITION BY country_code ORDER BY total_spent DESC) AS rank_num,
    ROUND(100 * total_spent / SUM(total_spent) OVER (PARTITION BY country_code), 2) AS pct_of_country
FROM customer_spend
QUALIFY rank_num <= 5
ORDER BY country_code, rank_num;

-- -----------------------------------------------------------------------------
-- 3. Raport miesięczny: LAG, dynamika, suma narastająca
-- -----------------------------------------------------------------------------
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', order_date) AS order_month,
        COUNT(*)                        AS orders_count,
        SUM(total_amount)               AS revenue
    FROM orders
    WHERE status <> 'CANCELLED'
    GROUP BY 1
)
SELECT
    order_month,
    orders_count,
    ROUND(revenue, 2)                                            AS revenue,
    ROUND(LAG(revenue) OVER (ORDER BY order_month), 2)           AS prev_revenue,
    ROUND(100 * (revenue - LAG(revenue) OVER (ORDER BY order_month))
          / NULLIF(LAG(revenue) OVER (ORDER BY order_month), 0), 2) AS growth_pct,
    ROUND(SUM(revenue) OVER (ORDER BY order_month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2)    AS running_total
FROM monthly
ORDER BY order_month;

-- -----------------------------------------------------------------------------
-- 4. Raport bez dziur – GENERATOR jako oś czasu
-- -----------------------------------------------------------------------------
WITH months AS (
    SELECT DATEADD('month', -SEQ4(), DATE_TRUNC('month', CURRENT_DATE())) AS month_start
    FROM TABLE(GENERATOR(ROWCOUNT => 12))
)
SELECT
    m.month_start,
    COALESCE(ROUND(SUM(o.total_amount), 2), 0) AS revenue
FROM months m
LEFT JOIN orders o
    ON DATE_TRUNC('month', o.order_date) = m.month_start
   AND o.status <> 'CANCELLED'
GROUP BY m.month_start
ORDER BY m.month_start;

-- -----------------------------------------------------------------------------
-- 5. VARIANT i FLATTEN – praca z JSON-em
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE events (
    event_id   NUMBER,
    event_time TIMESTAMP_LTZ,
    payload    VARIANT
);

INSERT INTO events (event_id, event_time, payload)
SELECT 1, CURRENT_TIMESTAMP(), PARSE_JSON('{
    "type": "order_created",
    "user": {"id": 42, "email": "anna@example.com", "country": "PL"},
    "items": [
        {"sku": "LAPTOP-01", "qty": 1, "price": 4999.00, "tags": ["premium", "sale"]},
        {"sku": "MOUSE-07",  "qty": 2, "price": 129.50, "tags": []}
    ],
    "total": 5258.00,
    "coupon": null
}');

INSERT INTO events (event_id, event_time, payload)
SELECT 2, CURRENT_TIMESTAMP(), PARSE_JSON('{
    "type": "order_created",
    "user": {"id": 43, "email": "jan@example.com", "country": "DE"},
    "items": [{"sku": "KEYBOARD-03", "qty": 1, "price": 349.00, "tags": ["sale"]}],
    "total": 349.00,
    "coupon": "SPRING10"
}');

-- Odczyt pól – rzutowanie przez :: jest obowiązkowe
SELECT
    event_id,
    payload:type::STRING        AS event_type,
    payload:user.id::NUMBER     AS user_id,
    payload:user.email::STRING  AS email,
    payload:total::NUMBER(12,2) AS total,
    ARRAY_SIZE(payload:items)   AS items_count
FROM events;

-- Rozbicie tablicy pozycji na wiersze
CREATE OR REPLACE TABLE analytics.order_lines AS
SELECT
    e.event_id,
    e.event_time,
    e.payload:user.id::NUMBER      AS user_id,
    e.payload:user.country::STRING AS country,
    item.value:sku::STRING         AS sku,
    item.value:qty::NUMBER         AS quantity,
    item.value:price::NUMBER(10,2) AS unit_price,
    item.value:qty::NUMBER * item.value:price::NUMBER(10,2) AS line_total
FROM events e,
     LATERAL FLATTEN(input => e.payload:items) AS item
WHERE e.payload:type::STRING = 'order_created';

SELECT * FROM analytics.order_lines;

-- Zagnieżdżony FLATTEN – unikalne tagi ze wszystkich pozycji
SELECT DISTINCT tag.value::STRING AS tag
FROM events e,
     LATERAL FLATTEN(input => e.payload:items) AS item,
     LATERAL FLATTEN(input => item.value:tags) AS tag;

-- Budowanie JSON-a w drugą stronę
SELECT OBJECT_CONSTRUCT(
    'customer_id', customer_id,
    'email',       email,
    'country',     country_code
) AS customer_json
FROM customers
LIMIT 3;

-- -----------------------------------------------------------------------------
-- 6. Time Travel
-- -----------------------------------------------------------------------------
-- UWAGA: AT(OFFSET => -N) działa tylko wtedy, gdy tabela istniała N sekund temu.
-- Jeśli uruchamiasz ten skrypt zaraz po 01_setup.sql, dostaniesz błąd
-- "Time travel data is not available" – odczekaj kilka minut albo zmniejsz offset.
-- DATA_RETENTION_TIME_IN_DAYS > 1 wymaga edycji Enterprise.
ALTER TABLE orders SET DATA_RETENTION_TIME_IN_DAYS = 3;

SELECT COUNT(*) AS rows_before FROM orders;

DELETE FROM orders WHERE status = 'CANCELLED';

SELECT COUNT(*) AS rows_after FROM orders;

-- Stan sprzed 5 minut
SELECT COUNT(*) AS rows_5_min_ago FROM orders AT(OFFSET => -60 * 5);

-- Przywrócenie usuniętych wierszy
INSERT INTO orders
SELECT * FROM orders AT(OFFSET => -60 * 5)
WHERE order_id NOT IN (SELECT order_id FROM orders);

-- UNDROP – odzyskanie usuniętej tabeli
DROP TABLE products;
SHOW TABLES HISTORY LIKE 'PRODUCTS';
UNDROP TABLE products;

-- -----------------------------------------------------------------------------
-- 7. Zero-copy cloning
-- -----------------------------------------------------------------------------
CREATE OR REPLACE DATABASE shop_db_dev CLONE shop_db;

-- Zmiana w klonie nie dotyka oryginału
USE DATABASE shop_db_dev;
DELETE FROM raw.orders;
SELECT COUNT(*) AS clone_rows FROM raw.orders;

USE DATABASE shop_db;
SELECT COUNT(*) AS original_rows FROM raw.orders;

-- Sprzątanie
DROP DATABASE shop_db_dev;
