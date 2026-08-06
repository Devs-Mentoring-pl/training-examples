-- =============================================================================
-- Szkolenie 5: Bezpieczeństwo, wydajność i koszty
-- =============================================================================
-- Wymaga wcześniejszego uruchomienia 01_setup.sql
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. Role – dwie warstwy: funkcyjne i dostępowe
-- -----------------------------------------------------------------------------
USE ROLE useradmin;

CREATE ROLE IF NOT EXISTS analyst       COMMENT = 'Odczyt warstwy analitycznej';
CREATE ROLE IF NOT EXISTS data_engineer COMMENT = 'Budowa pipeline''ów';

CREATE ROLE IF NOT EXISTS shop_db_analytics_read;
CREATE ROLE IF NOT EXISTS shop_db_raw_write;

-- Role dostępowe wpinamy w funkcyjne
GRANT ROLE shop_db_analytics_read TO ROLE analyst;
GRANT ROLE shop_db_analytics_read TO ROLE data_engineer;
GRANT ROLE shop_db_raw_write      TO ROLE data_engineer;

-- Wszystko podpinamy pod SYSADMIN – inaczej admin nie zobaczy obiektów
GRANT ROLE analyst       TO ROLE sysadmin;
GRANT ROLE data_engineer TO ROLE sysadmin;

-- -----------------------------------------------------------------------------
-- 2. Użytkownicy
-- -----------------------------------------------------------------------------
CREATE USER IF NOT EXISTS anna
    PASSWORD = 'TymczasoweHaslo123!'
    MUST_CHANGE_PASSWORD = TRUE
    DEFAULT_ROLE = 'ANALYST'
    DEFAULT_WAREHOUSE = 'LEARN_WH'
    COMMENT = 'Analityk danych';

-- Konto serwisowe: bez hasła, wyłącznie klucz RSA
-- CREATE USER IF NOT EXISTS svc_etl
--     TYPE = SERVICE
--     RSA_PUBLIC_KEY = 'MIIBIjANBgkq...'
--     DEFAULT_ROLE = 'DATA_ENGINEER'
--     DEFAULT_WAREHOUSE = 'LEARN_WH';

GRANT ROLE analyst TO USER anna;

-- -----------------------------------------------------------------------------
-- 3. Uprawnienia – pamiętaj o USAGE na każdym szczeblu
-- -----------------------------------------------------------------------------
USE ROLE securityadmin;

GRANT USAGE ON WAREHOUSE learn_wh          TO ROLE shop_db_analytics_read;
GRANT USAGE ON DATABASE shop_db            TO ROLE shop_db_analytics_read;
GRANT USAGE ON SCHEMA shop_db.analytics    TO ROLE shop_db_analytics_read;

GRANT SELECT ON ALL TABLES IN SCHEMA shop_db.analytics TO ROLE shop_db_analytics_read;
GRANT SELECT ON ALL VIEWS  IN SCHEMA shop_db.analytics TO ROLE shop_db_analytics_read;

-- Future grants – dostęp do obiektów utworzonych w PRZYSZŁOŚCI
GRANT SELECT ON FUTURE TABLES IN SCHEMA shop_db.analytics TO ROLE shop_db_analytics_read;
GRANT SELECT ON FUTURE VIEWS  IN SCHEMA shop_db.analytics TO ROLE shop_db_analytics_read;

-- Rola inżynierska – pełne prawa do warstwy RAW
GRANT USAGE ON WAREHOUSE learn_wh TO ROLE shop_db_raw_write;
GRANT USAGE ON DATABASE shop_db   TO ROLE shop_db_raw_write;
GRANT ALL ON SCHEMA shop_db.raw   TO ROLE shop_db_raw_write;
GRANT ALL ON ALL TABLES IN SCHEMA shop_db.raw TO ROLE shop_db_raw_write;

-- Weryfikacja
SHOW GRANTS TO ROLE analyst;
SHOW GRANTS TO ROLE shop_db_analytics_read;
SHOW FUTURE GRANTS IN SCHEMA shop_db.analytics;

-- -----------------------------------------------------------------------------
-- 4. Maskowanie danych (Enterprise)
-- -----------------------------------------------------------------------------
USE ROLE sysadmin;

-- Jeśli dostaniesz błąd o braku uprawnień do zastosowania polityki, nadaj je raz:
--   USE ROLE accountadmin;
--   GRANT APPLY MASKING POLICY ON ACCOUNT TO ROLE sysadmin;
CREATE OR REPLACE MASKING POLICY email_mask AS (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('ACCOUNTADMIN', 'SYSADMIN', 'DATA_ENGINEER') THEN val
        WHEN CURRENT_ROLE() = 'ANALYST' THEN REGEXP_REPLACE(val, '^[^@]+', '****')
        ELSE '***MASKED***'
    END;

ALTER TABLE shop_db.raw.customers MODIFY COLUMN email SET MASKING POLICY email_mask;

-- Test: to samo zapytanie, różne wyniki zależnie od roli
SELECT email FROM shop_db.raw.customers LIMIT 3;

-- Odpięcie
-- ALTER TABLE shop_db.raw.customers MODIFY COLUMN email UNSET MASKING POLICY;

-- -----------------------------------------------------------------------------
-- 5. Tagi – klasyfikacja danych osobowych
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TAG pii_level COMMENT = 'Poziom wrażliwości danych osobowych';

ALTER TABLE shop_db.raw.customers MODIFY COLUMN email        SET TAG pii_level = 'HIGH';
ALTER TABLE shop_db.raw.customers MODIFY COLUMN country_code SET TAG pii_level = 'LOW';

-- -----------------------------------------------------------------------------
-- 6. Wydajność – mikropartycje i pruning
-- -----------------------------------------------------------------------------
-- Wyłączamy result cache, żeby mierzyć faktyczne wykonanie
ALTER SESSION SET USE_CACHED_RESULT = FALSE;

-- ❌ Funkcja na kolumnie filtrowanej blokuje pruning
SELECT SUM(total_amount)
FROM shop_db.raw.orders
WHERE TO_CHAR(order_date, 'YYYY-MM') = '2026-08';

-- ✅ Filtr na surowej kolumnie – pruning działa
SELECT SUM(total_amount)
FROM shop_db.raw.orders
WHERE order_date >= '2026-08-01' AND order_date < '2026-09-01';

-- Porównaj partitions_scanned obu zapytań w Query History

-- Jakość uporządkowania danych w tabeli
SELECT SYSTEM$CLUSTERING_INFORMATION('shop_db.raw.orders', '(order_date)');

ALTER SESSION SET USE_CACHED_RESULT = TRUE;

-- -----------------------------------------------------------------------------
-- 7. Audyt wydajności
-- -----------------------------------------------------------------------------
USE ROLE accountadmin;

-- Najwolniejsze zapytania z ostatniej doby wraz ze spillem
SELECT
    query_id,
    user_name,
    warehouse_name,
    warehouse_size,
    ROUND(total_elapsed_time / 1000, 1)                        AS seconds,
    ROUND(bytes_scanned / POWER(1024, 3), 2)                   AS gb_scanned,
    partitions_scanned,
    partitions_total,
    ROUND(bytes_spilled_to_local_storage  / POWER(1024, 3), 2) AS gb_spilled_local,
    ROUND(bytes_spilled_to_remote_storage / POWER(1024, 3), 2) AS gb_spilled_remote,
    LEFT(query_text, 100)                                      AS query_snippet
FROM snowflake.account_usage.query_history
WHERE start_time >= DATEADD('day', -1, CURRENT_TIMESTAMP())
  AND total_elapsed_time > 5000
ORDER BY total_elapsed_time DESC
LIMIT 20;

-- -----------------------------------------------------------------------------
-- 8. Audyt kosztów
-- -----------------------------------------------------------------------------

-- Kredyty według warehouse'ów (ostatnie 30 dni)
SELECT
    warehouse_name,
    ROUND(SUM(credits_used), 2)                AS total_credits,
    ROUND(SUM(credits_used_compute), 2)        AS compute_credits,
    ROUND(SUM(credits_used_cloud_services), 2) AS cloud_services_credits
FROM snowflake.account_usage.warehouse_metering_history
WHERE start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP())
GROUP BY warehouse_name
ORDER BY total_credits DESC;

-- Storage: aktywny vs Time Travel vs fail-safe
SELECT
    table_catalog || '.' || table_schema || '.' || table_name AS full_name,
    ROUND(active_bytes      / POWER(1024, 3), 3) AS active_gb,
    ROUND(time_travel_bytes / POWER(1024, 3), 3) AS time_travel_gb,
    ROUND(failsafe_bytes    / POWER(1024, 3), 3) AS failsafe_gb
FROM snowflake.account_usage.table_storage_metrics
WHERE deleted = FALSE
ORDER BY active_bytes DESC
LIMIT 20;

-- Nieudane logowania – podstawowy audyt bezpieczeństwa
SELECT event_timestamp, user_name, client_ip, first_authentication_factor, error_message
FROM snowflake.account_usage.login_history
WHERE is_success = 'NO'
  AND event_timestamp >= DATEADD('day', -7, CURRENT_TIMESTAMP())
ORDER BY event_timestamp DESC;

-- -----------------------------------------------------------------------------
-- 9. Limity ochronne
-- -----------------------------------------------------------------------------
USE ROLE sysadmin;

ALTER WAREHOUSE learn_wh SET STATEMENT_TIMEOUT_IN_SECONDS = 900;         -- 15 minut
ALTER WAREHOUSE learn_wh SET STATEMENT_QUEUED_TIMEOUT_IN_SECONDS = 300;  -- 5 minut w kolejce
ALTER WAREHOUSE learn_wh SUSPEND;
