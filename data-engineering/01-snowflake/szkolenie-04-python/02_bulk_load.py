"""Masowy zapis do Snowflake: executemany vs write_pandas vs PUT + COPY INTO.

Skrypt mierzy czas każdej metody na tym samym zbiorze danych.

Uruchomienie:
    python 02_bulk_load.py
"""

from __future__ import annotations

import random
import time
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
from snowflake.connector.pandas_tools import write_pandas

from connection import get_connection

ROWS = 50_000
TARGET_TABLE = "BULK_TEST"


def generate_orders(n: int) -> pd.DataFrame:
    """Generuje losowe zamówienia. Nazwy kolumn WIELKIMI literami – patrz write_pandas."""
    today = date.today()
    return pd.DataFrame(
        {
            "ORDER_ID": range(1, n + 1),
            "CUSTOMER_ID": [random.randint(1, 200) for _ in range(n)],
            "ORDER_DATE": [today - timedelta(days=random.randint(0, 730)) for _ in range(n)],
            "STATUS": [random.choice(["NEW", "PAID", "SHIPPED"]) for _ in range(n)],
            "TOTAL_AMOUNT": [round(random.uniform(50, 8000), 2) for _ in range(n)],
        }
    )


def create_target_table(conn) -> None:
    """Tworzy pustą tabelę docelową."""
    with conn.cursor() as cur:
        cur.execute(f"""
            CREATE OR REPLACE TABLE shop_db.raw.{TARGET_TABLE} (
                order_id     NUMBER,
                customer_id  NUMBER,
                order_date   DATE,
                status       VARCHAR(20),
                total_amount NUMBER(12,2)
            )
        """)


def load_with_executemany(conn, df: pd.DataFrame) -> float:
    """Wariant naiwny – wiele osobnych INSERT-ów. Wolny, tworzy mnóstwo mikropartycji."""
    create_target_table(conn)
    rows = [tuple(row) for row in df.itertuples(index=False)]

    start = time.perf_counter()
    with conn.cursor() as cur:
        cur.executemany(
            f"INSERT INTO shop_db.raw.{TARGET_TABLE} "
            "(order_id, customer_id, order_date, status, total_amount) "
            "VALUES (%s, %s, %s, %s, %s)",
            rows,
        )
    return time.perf_counter() - start


def load_with_write_pandas(conn, df: pd.DataFrame) -> float:
    """Wariant właściwy – Parquet na stage + COPY INTO pod spodem."""
    create_target_table(conn)

    start = time.perf_counter()
    success, _, num_rows, _ = write_pandas(
        conn=conn,
        df=df,
        table_name=TARGET_TABLE,
        database="SHOP_DB",
        schema="RAW",
        quote_identifiers=False,   # bez tego kolumny trafią w cudzysłowach i nie dopasują się
        chunk_size=100_000,
    )
    elapsed = time.perf_counter() - start

    if not success:
        raise RuntimeError("write_pandas nie powiodło się")
    print(f"  write_pandas zapisał {num_rows} wierszy")
    return elapsed


def load_with_put_copy(conn, df: pd.DataFrame, tmp_dir: Path) -> float:
    """Wariant plikowy – zapis CSV, PUT na stage, COPY INTO."""
    create_target_table(conn)

    csv_path = tmp_dir / "bulk_orders.csv"
    df.to_csv(csv_path, index=False)

    start = time.perf_counter()
    with conn.cursor() as cur:
        cur.execute("CREATE STAGE IF NOT EXISTS shop_db.raw.bulk_stage")
        cur.execute(
            f"PUT file://{csv_path.resolve()} @shop_db.raw.bulk_stage "
            "AUTO_COMPRESS=TRUE OVERWRITE=TRUE"
        )
        cur.execute(f"""
            COPY INTO shop_db.raw.{TARGET_TABLE}
            FROM @shop_db.raw.bulk_stage/{csv_path.name}.gz
            FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '"')
            ON_ERROR = 'CONTINUE'
        """)
        for row in cur.fetchall():
            print(f"  COPY INTO: {row}")
        cur.execute(f"REMOVE @shop_db.raw.bulk_stage/{csv_path.name}.gz")
    return time.perf_counter() - start


if __name__ == "__main__":
    tmp_dir = Path(__file__).parent / "tmp"
    tmp_dir.mkdir(exist_ok=True)

    df = generate_orders(ROWS)
    print(f"Wygenerowano {len(df)} wierszy\n")

    with get_connection() as conn:
        print("1. executemany()")
        t_many = load_with_executemany(conn, df)
        print(f"   czas: {t_many:.2f} s\n")

        print("2. write_pandas()")
        t_pandas = load_with_write_pandas(conn, df)
        print(f"   czas: {t_pandas:.2f} s\n")

        print("3. PUT + COPY INTO")
        t_copy = load_with_put_copy(conn, df, tmp_dir)
        print(f"   czas: {t_copy:.2f} s\n")

        print(f"write_pandas był {t_many / t_pandas:.1f}x szybszy od executemany()")

        with conn.cursor() as cur:
            cur.execute(f"DROP TABLE IF EXISTS shop_db.raw.{TARGET_TABLE}")
