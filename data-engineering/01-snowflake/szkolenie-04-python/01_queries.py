"""Podstawy pracy z snowflake-connector-python: kursory, parametryzacja, pandas.

Uruchomienie:
    python 01_queries.py
"""

from __future__ import annotations

from snowflake.connector import DictCursor

from connection import get_connection


def count_customers(conn) -> int:
    """Zwraca liczbę klientów w tabeli."""
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM shop_db.raw.customers")
        (total,) = cur.fetchone()
        return total


def get_top_customers(conn, country: str, limit: int = 10) -> list[dict]:
    """Zwraca najlepszych klientów z danego kraju wraz z ich wydatkami.

    Zapytanie jest parametryzowane – konkatenacja stringów oznaczałaby SQL Injection.
    """
    query = """
        SELECT
            c.customer_id,
            c.email,
            COUNT(o.order_id)                AS orders_count,
            ROUND(SUM(o.total_amount), 2)    AS total_spent
        FROM shop_db.raw.customers c
        JOIN shop_db.raw.orders o ON o.customer_id = c.customer_id
        WHERE c.country_code = %(country)s
          AND o.status <> 'CANCELLED'
        GROUP BY c.customer_id, c.email
        ORDER BY total_spent DESC
        LIMIT %(limit)s
    """
    with conn.cursor(DictCursor) as cur:
        cur.execute(query, {"country": country, "limit": limit})
        return cur.fetchall()


def revenue_by_country(conn):
    """Zwraca przychód według krajów jako pandas.DataFrame."""
    query = """
        SELECT
            c.country_code,
            COUNT(DISTINCT c.customer_id) AS customers,
            ROUND(SUM(o.total_amount), 2) AS revenue
        FROM shop_db.raw.customers c
        LEFT JOIN shop_db.raw.orders o ON o.customer_id = c.customer_id
        GROUP BY c.country_code
        ORDER BY revenue DESC NULLS LAST
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetch_pandas_all()


def stream_large_result(conn) -> int:
    """Czyta duży wynik porcjami, żeby nie zająć całej pamięci RAM."""
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM snowflake_sample_data.tpch_sf1.orders")

        total_rows = 0
        for chunk in cur.fetch_pandas_batches():
            total_rows += len(chunk)
        return total_rows


if __name__ == "__main__":
    with get_connection() as conn:
        print(f"Klientów w bazie: {count_customers(conn)}")

        print("\nTop 5 klientów z Polski:")
        for row in get_top_customers(conn, country="PL", limit=5):
            print(f"  {row['EMAIL']:<35} {row['ORDERS_COUNT']:>3} zam.  {row['TOTAL_SPENT']:>12}")

        # Próba wstrzyknięcia SQL – parametryzacja sprawia, że to zwykły, pusty wynik
        malicious = "PL'; DROP TABLE customers; --"
        print(f"\nPróba SQL Injection zwróciła {len(get_top_customers(conn, malicious))} wierszy")

        print("\nPrzychód według krajów:")
        print(revenue_by_country(conn).to_string(index=False))

        print(f"\nPrzeczytano porcjami {stream_large_result(conn)} wierszy z TPCH_SF1")
