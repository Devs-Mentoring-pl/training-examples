-- =============================================================================
-- Szkolenie 3: Ładowanie i przetwarzanie danych
-- =============================================================================
-- Wymaga wcześniejszego uruchomienia 01_setup.sql
-- Pliki na stage wgrywasz przez Snowsight (Data -> Databases -> stage -> + Files)
-- albo komendą PUT ze Snowflake CLI (patrz README).
-- =============================================================================

USE ROLE sysadmin;
USE WAREHOUSE learn_wh;
USE DATABASE shop_db;
USE SCHEMA raw;

-- -----------------------------------------------------------------------------
-- 1. Stage i formaty plików
-- -----------------------------------------------------------------------------
CREATE OR REPLACE STAGE shop_stage
    DIRECTORY = (ENABLE = TRUE)
    COMMENT = 'Pliki wejściowe sklepu';

CREATE OR REPLACE FILE FORMAT csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('', 'NULL', 'null', '\\N')
    EMPTY_FIELD_AS_NULL = TRUE
    TRIM_SPACE = TRUE
    DATE_FORMAT = 'YYYY-MM-DD'
    ENCODING = 'UTF8'
    COMPRESSION = 'AUTO';

CREATE OR REPLACE FILE FORMAT json_format
    TYPE = 'JSON'
    STRIP_OUTER_ARRAY = TRUE       -- rozbij zewnętrzną tablicę na osobne dokumenty
    COMPRESSION = 'AUTO';

CREATE OR REPLACE FILE FORMAT parquet_format TYPE = 'PARQUET';

LIST @shop_stage;

-- -----------------------------------------------------------------------------
-- 2. Podgląd pliku PRZED załadowaniem
-- -----------------------------------------------------------------------------
-- $1, $2, ... to kolejne kolumny pliku
SELECT
    METADATA$FILENAME        AS source_file,
    METADATA$FILE_ROW_NUMBER AS row_in_file,
    $1, $2, $3, $4
FROM @shop_stage/customers.csv (FILE_FORMAT => csv_format)
LIMIT 10;

-- -----------------------------------------------------------------------------
-- 3. Walidacja bez ładowania
-- -----------------------------------------------------------------------------
COPY INTO customers
FROM @shop_stage/customers.csv
FILE_FORMAT = (FORMAT_NAME = csv_format)
VALIDATION_MODE = 'RETURN_ERRORS';

-- -----------------------------------------------------------------------------
-- 4. Ładowanie z transformacją w locie
-- -----------------------------------------------------------------------------
COPY INTO customers (customer_id, email, first_name, last_name, country_code, signup_date)
FROM (
    SELECT
        $1::NUMBER                    AS customer_id,
        LOWER(TRIM($2))               AS email,
        INITCAP($3)                   AS first_name,
        INITCAP($4)                   AS last_name,
        UPPER($5)                     AS country_code,
        TRY_TO_DATE($6, 'YYYY-MM-DD') AS signup_date  -- błędna data -> NULL, nie błąd
    FROM @shop_stage/customers.csv
)
FILE_FORMAT = (FORMAT_NAME = csv_format)
ON_ERROR = 'CONTINUE';

-- -----------------------------------------------------------------------------
-- 5. Odrzucone wiersze
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE customers_rejects (
    source_file   VARCHAR,
    row_number    NUMBER,
    error_message VARCHAR,
    raw_row       VARIANT,
    loaded_at     TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP()
);

INSERT INTO customers_rejects (source_file, row_number, error_message, raw_row)
SELECT
    file,
    row_number,
    error,
    OBJECT_CONSTRUCT('rejected_record', rejected_record)
FROM TABLE(VALIDATE(customers, JOB_ID => '_last'));

SELECT * FROM customers_rejects;

-- Historia ładowań
SELECT *
FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'shop_db.raw.customers',
    START_TIME => DATEADD('hour', -24, CURRENT_TIMESTAMP())
));

-- -----------------------------------------------------------------------------
-- 6. Ładowanie JSON-a do kolumny VARIANT
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE raw_events (
    payload     VARIANT,
    source_file VARCHAR,
    loaded_at   TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP()
);

COPY INTO raw_events (payload, source_file)
FROM (
    SELECT $1, METADATA$FILENAME
    FROM @shop_stage/events.json
)
FILE_FORMAT = (FORMAT_NAME = json_format);

-- Rozbicie dopiero w hurtowni (podejście ELT)
CREATE OR REPLACE TABLE staging.events_parsed AS
SELECT
    payload:type::STRING             AS event_type,
    payload:user.id::NUMBER          AS user_id,
    payload:total::NUMBER(12,2)      AS total,
    source_file
FROM raw_events;

-- -----------------------------------------------------------------------------
-- 7. Stream – śledzenie zmian (CDC)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE STREAM orders_stream ON TABLE orders;

INSERT INTO orders (order_id, customer_id, order_date, status, total_amount)
VALUES (999001, 1, CURRENT_DATE(), 'NEW', 299.00);

UPDATE orders SET status = 'PAID' WHERE order_id = 999001;

-- UPDATE widoczny jest jako para DELETE + INSERT z flagą METADATA$ISUPDATE
SELECT
    order_id,
    status,
    METADATA$ACTION   AS action,
    METADATA$ISUPDATE AS is_update
FROM orders_stream;

SELECT SYSTEM$STREAM_HAS_DATA('orders_stream') AS has_data;

-- -----------------------------------------------------------------------------
-- 8. Task – harmonogram
-- -----------------------------------------------------------------------------
-- Tabele docelowe muszą istnieć, zanim utworzymy taski, które do nich piszą
CREATE TABLE IF NOT EXISTS staging.orders_clean (
    order_id     NUMBER,
    customer_id  NUMBER,
    order_date   DATE,
    status       VARCHAR(20),
    total_amount NUMBER(12,2)
);

CREATE TABLE IF NOT EXISTS analytics.daily_revenue (
    order_date   DATE,
    orders_count NUMBER,
    revenue      NUMBER(14,2)
);

CREATE OR REPLACE TASK load_orders_task
    WAREHOUSE = learn_wh
    SCHEDULE = '5 MINUTE'
    WHEN SYSTEM$STREAM_HAS_DATA('orders_stream')
AS
    MERGE INTO staging.orders_clean AS t
    USING orders_stream AS s
        ON t.order_id = s.order_id
    -- UPDATE w streamie to DELETE + INSERT z ISUPDATE = TRUE.
    -- Bez rozróżnienia po ISUPDATE oba wiersze trafiłyby w ten sam wiersz docelowy
    -- i MERGE zwróciłby błąd "Duplicate row detected during DML action".
    WHEN MATCHED AND s.METADATA$ACTION = 'DELETE' AND s.METADATA$ISUPDATE = FALSE THEN
        DELETE
    WHEN MATCHED AND s.METADATA$ACTION = 'INSERT' AND s.METADATA$ISUPDATE = TRUE THEN
        UPDATE SET t.status = s.status, t.total_amount = s.total_amount
    WHEN NOT MATCHED AND s.METADATA$ACTION = 'INSERT' THEN
        INSERT (order_id, customer_id, order_date, status, total_amount)
        VALUES (s.order_id, s.customer_id, s.order_date, s.status, s.total_amount);

CREATE OR REPLACE TASK aggregate_daily_task
    WAREHOUSE = learn_wh
    AFTER load_orders_task
AS
    INSERT OVERWRITE INTO analytics.daily_revenue
    SELECT order_date, COUNT(*) AS orders_count, SUM(total_amount) AS revenue
    FROM staging.orders_clean
    GROUP BY order_date;

-- Uruchamiamy od liści do korzenia!
ALTER TASK aggregate_daily_task RESUME;
ALTER TASK load_orders_task RESUME;

SHOW TASKS;

-- Historia wykonań
SELECT name, state, scheduled_time, completed_time, error_message
FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY(
    SCHEDULED_TIME_RANGE_START => DATEADD('hour', -2, CURRENT_TIMESTAMP())
))
ORDER BY scheduled_time DESC;

-- Zatrzymanie – odwrotna kolejność
ALTER TASK load_orders_task SUSPEND;
ALTER TASK aggregate_daily_task SUSPEND;

-- -----------------------------------------------------------------------------
-- 9. Dynamic table – to samo, deklaratywnie
-- -----------------------------------------------------------------------------
CREATE OR REPLACE DYNAMIC TABLE analytics.customer_summary
    TARGET_LAG = '1 hour'
    WAREHOUSE = learn_wh
AS
SELECT
    c.customer_id,
    c.email,
    c.country_code,
    COUNT(o.order_id)                AS orders_count,
    COALESCE(SUM(o.total_amount), 0) AS lifetime_value,
    MAX(o.order_date)                AS last_order_date
FROM raw.customers c
LEFT JOIN raw.orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.email, c.country_code;

ALTER DYNAMIC TABLE analytics.customer_summary REFRESH;

SELECT * FROM analytics.customer_summary ORDER BY lifetime_value DESC LIMIT 10;

SELECT *
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
    NAME => 'analytics.customer_summary'
))
ORDER BY refresh_start_time DESC;

-- -----------------------------------------------------------------------------
-- 10. Eksport danych
-- -----------------------------------------------------------------------------
COPY INTO @shop_stage/export/customer_summary_
FROM analytics.customer_summary
FILE_FORMAT = (TYPE = 'PARQUET')
HEADER = TRUE
OVERWRITE = TRUE;

LIST @shop_stage/export/;
