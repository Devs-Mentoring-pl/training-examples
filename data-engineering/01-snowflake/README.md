# Snowflake – przykłady

Kod do szkoleń 1–5 ze Snowflake (ścieżka Python Backend Developer).

## Struktura

- `sql/01_setup.sql` — warehouse, resource monitor, baza, schematy, dane testowe
- `sql/02_sql_basics.sql` — DDL/DML, funkcje okna, VARIANT/FLATTEN, Time Travel, klonowanie
- `sql/03_loading.sql` — file formaty, stage, COPY INTO, stream, task, dynamic table
- `sql/05_security_cost.sql` — role, granty, maskowanie, audyt wydajności i kosztów
- `szkolenie-04-python/` — connector, pandas, Snowpark, UDF, procedury

Numeracja plików SQL odpowiada numerom szkoleń (dla szkolenia 4 kod jest w Pythonie).

## Wymagania

- konto Snowflake (wystarczy 30-dniowy trial: https://signup.snowflake.com/)
- Python 3.10+ dla przykładów z `szkolenie-04-python/`

## Uruchamianie SQL

Skrypty wklejasz do arkusza w Snowsight albo uruchamiasz przez Snowflake CLI:

```bash
pip install snowflake-cli
snow connection add          # konfiguracja połączenia
snow sql -f sql/01_setup.sql
```

> Skrypty uruchamiaj w kolejności numerów – `01_setup.sql` tworzy obiekty używane przez pozostałe.

## Koszty

Wszystkie przykłady działają na warehousie `XSMALL` z `AUTO_SUSPEND = 60`.
`01_setup.sql` tworzy resource monitor z limitem 10 kredytów – zostaw go włączonego.
