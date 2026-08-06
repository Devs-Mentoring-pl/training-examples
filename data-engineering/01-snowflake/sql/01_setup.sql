-- =============================================================================
-- Szkolenie 1: Wprowadzenie do Snowflake – konfiguracja środowiska
-- =============================================================================
-- Uruchom ten skrypt jako pierwszy. Tworzy warehouse, resource monitor,
-- bazę ze schematami oraz dane testowe używane w pozostałych skryptach.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. Warehouse do nauki
-- -----------------------------------------------------------------------------
USE ROLE sysadmin;

CREATE WAREHOUSE IF NOT EXISTS learn_wh
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60              -- uśpij po minucie bezczynności
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Warehouse do nauki – szkolenie Snowflake';

USE WAREHOUSE learn_wh;

-- Sprawdzenie kontekstu sesji
SELECT
    CURRENT_ROLE()      AS role,
    CURRENT_WAREHOUSE() AS warehouse,
    CURRENT_USER()      AS user,
    CURRENT_VERSION()   AS snowflake_version;

-- -----------------------------------------------------------------------------
-- 2. Resource monitor – bezpiecznik na kredyty
-- -----------------------------------------------------------------------------
USE ROLE accountadmin;

CREATE RESOURCE MONITOR IF NOT EXISTS learn_monitor
    WITH CREDIT_QUOTA = 10
    FREQUENCY = MONTHLY
    START_TIMESTAMP = IMMEDIATELY
    TRIGGERS
        ON 75  PERCENT DO NOTIFY
        ON 100 PERCENT DO SUSPEND
        ON 110 PERCENT DO SUSPEND_IMMEDIATE;

ALTER WAREHOUSE learn_wh SET RESOURCE_MONITOR = learn_monitor;

USE ROLE sysadmin;

-- -----------------------------------------------------------------------------
-- 3. Baza i schematy – warstwy przetwarzania
-- -----------------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS shop_db
    COMMENT = 'Baza szkoleniowa – dane sklepu internetowego';

USE DATABASE shop_db;

CREATE SCHEMA IF NOT EXISTS raw       COMMENT = 'Dane surowe ze źródeł';
CREATE SCHEMA IF NOT EXISTS staging   COMMENT = 'Dane po czyszczeniu';
CREATE SCHEMA IF NOT EXISTS analytics COMMENT = 'Modele analityczne dla BI';

-- -----------------------------------------------------------------------------
-- 4. Tabele warstwy RAW
-- -----------------------------------------------------------------------------
USE SCHEMA raw;

CREATE OR REPLACE TABLE customers (
    customer_id  NUMBER(38,0)  NOT NULL,
    email        VARCHAR(255)  NOT NULL,
    first_name   VARCHAR(100),
    last_name    VARCHAR(100),
    country_code VARCHAR(2),
    signup_date  DATE,
    is_active    BOOLEAN       DEFAULT TRUE,
    created_at   TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE OR REPLACE TABLE products (
    product_id NUMBER(38,0) NOT NULL,
    name       VARCHAR(255) NOT NULL,
    category   VARCHAR(100),
    price      NUMBER(10,2) NOT NULL,
    in_stock   NUMBER(38,0) DEFAULT 0
);

CREATE OR REPLACE TABLE orders (
    order_id     NUMBER(38,0) NOT NULL,
    customer_id  NUMBER(38,0) NOT NULL,
    order_date   DATE         NOT NULL,
    status       VARCHAR(20)  DEFAULT 'NEW',
    total_amount NUMBER(12,2)
);

CREATE OR REPLACE TABLE order_items (
    order_item_id NUMBER(38,0) NOT NULL,
    order_id      NUMBER(38,0) NOT NULL,
    product_id    NUMBER(38,0) NOT NULL,
    quantity      NUMBER(38,0) NOT NULL,
    unit_price    NUMBER(10,2) NOT NULL
);

-- -----------------------------------------------------------------------------
-- 5. Dane testowe generowane zapytaniem (bez ręcznego wpisywania)
-- -----------------------------------------------------------------------------

-- UWAGA: SEQ4() wywołane kilka razy w jednym SELECT generuje NIEZALEŻNE sekwencje.
-- Dlatego numer wiersza liczymy raz w podzapytaniu i dopiero go używamy.

-- 200 klientów z 5 krajów
INSERT INTO customers (customer_id, email, first_name, last_name, country_code, signup_date)
SELECT
    n                                                   AS customer_id,
    'user' || n || '@example.com'                       AS email,
    'Imie' || n                                         AS first_name,
    'Nazwisko' || n                                     AS last_name,
    GET(ARRAY_CONSTRUCT('PL', 'DE', 'ES', 'GB', 'FR'),
        UNIFORM(0, 4, RANDOM()))::VARCHAR               AS country_code,
    DATEADD('day', -UNIFORM(1, 730, RANDOM()), CURRENT_DATE()) AS signup_date
FROM (SELECT SEQ4() + 1 AS n FROM TABLE(GENERATOR(ROWCOUNT => 200)));

-- 50 produktów w 4 kategoriach
INSERT INTO products (product_id, name, category, price, in_stock)
SELECT
    n                                                   AS product_id,
    'Produkt ' || n                                     AS name,
    GET(ARRAY_CONSTRUCT('Electronics', 'Accessories', 'Home', 'Sport'),
        UNIFORM(0, 3, RANDOM()))::VARCHAR               AS category,
    ROUND(UNIFORM(20::FLOAT, 5000::FLOAT, RANDOM()), 2) AS price,
    UNIFORM(0, 500, RANDOM())                           AS in_stock
FROM (SELECT SEQ4() + 1 AS n FROM TABLE(GENERATOR(ROWCOUNT => 50)));

-- 2000 zamówień z ostatnich 24 miesięcy
INSERT INTO orders (order_id, customer_id, order_date, status, total_amount)
SELECT
    n                                                   AS order_id,
    UNIFORM(1, 200, RANDOM())                           AS customer_id,
    DATEADD('day', -UNIFORM(1, 730, RANDOM()), CURRENT_DATE()) AS order_date,
    GET(ARRAY_CONSTRUCT('NEW', 'PAID', 'SHIPPED', 'CANCELLED'),
        UNIFORM(0, 3, RANDOM()))::VARCHAR               AS status,
    ROUND(UNIFORM(50::FLOAT, 8000::FLOAT, RANDOM()), 2) AS total_amount
FROM (SELECT SEQ4() + 1 AS n FROM TABLE(GENERATOR(ROWCOUNT => 2000)));

-- 5000 pozycji zamówień
INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price)
SELECT
    n                                                   AS order_item_id,
    UNIFORM(1, 2000, RANDOM())                          AS order_id,
    UNIFORM(1, 50, RANDOM())                            AS product_id,
    UNIFORM(1, 5, RANDOM())                             AS quantity,
    ROUND(UNIFORM(20::FLOAT, 5000::FLOAT, RANDOM()), 2) AS unit_price
FROM (SELECT SEQ4() + 1 AS n FROM TABLE(GENERATOR(ROWCOUNT => 5000)));

-- -----------------------------------------------------------------------------
-- 6. Weryfikacja
-- -----------------------------------------------------------------------------
SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL SELECT 'products',    COUNT(*) FROM products
UNION ALL SELECT 'orders',      COUNT(*) FROM orders
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items;

-- Pamiętaj o zatrzymaniu warehouse'a po pracy
-- ALTER WAREHOUSE learn_wh SUSPEND;
