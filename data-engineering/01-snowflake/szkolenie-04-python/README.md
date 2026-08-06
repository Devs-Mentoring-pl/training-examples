# Szkolenie 4: Snowflake i Python

Przyklady polaczenia Snowflake z Pythonem: connector (DB-API), pandas, Snowpark,
UDF-y i procedury skladowane.

## Pliki

- `connection.py` -- wspolna konfiguracja polaczenia (haslo / klucz RSA / przegladarka)
- `01_queries.py` -- kursory, parametryzacja, DictCursor, fetch_pandas
- `02_bulk_load.py` -- porownanie executemany vs write_pandas vs PUT + COPY INTO
- `03_snowpark.py` -- DataFrame API wykonywane po stronie Snowflake
- `04_udf_procedure.py` -- UDF-y w Pythonie i procedura skladowana

## Wymagania

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env    # uzupelnij dane konta
```

Przed uruchomieniem skryptow wykonaj `../sql/01_setup.sql` -- tworzy baze i dane testowe.

## Uwierzytelnianie

Konta serwisowe nie moga logowac sie samym haslem. Wygeneruj klucz RSA:

```bash
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -nocrypt -out snowflake_key.p8
openssl rsa -in snowflake_key.p8 -pubout -out snowflake_key.pub
chmod 600 snowflake_key.p8
```

Zawartosc `snowflake_key.pub` (bez linii BEGIN/END i bez znakow nowej linii) przypisz uzytkownikowi:

```sql
ALTER USER twoj_uzytkownik SET RSA_PUBLIC_KEY = 'MIIBIjANBgkq...';
```

Nastepnie ustaw `SNOWFLAKE_PRIVATE_KEY_PATH` w `.env`.

> Pliki `.env` oraz `*.p8` nigdy nie trafiaja do repozytorium.

## Uruchomienie

```bash
python connection.py        # test polaczenia
python 01_queries.py
python 02_bulk_load.py
python 03_snowpark.py
python 04_udf_procedure.py
```
