"""
Szkolenie 3 SQLite3 w Pythonie - Przyklad 5
Baza w pamieci (:memory:), skrocona forma z with sqlite3.connect().
"""

import sqlite3
from contextlib import closing


def demo_memory_database() -> None:
    """Demonstracja bazy danych w pamieci RAM."""
    print("=== Baza w pamieci (:memory:) ===")

    with sqlite3.connect(":memory:") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # Tworzenie tabeli
        cursor.execute("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER DEFAULT 0
            )
        """)

        # Wstawianie danych
        products = [
            ("Laptop", 3999.99, 10),
            ("Mysz", 129.99, 50),
            ("Klawiatura", 249.99, 30),
            ("Monitor", 1499.99, 15),
            ("Sluchawki", 399.99, 25),
        ]

        cursor.executemany(
            "INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)",
            products
        )

        # Zapytania
        print("\nWszystkie produkty:")
        cursor.execute("SELECT * FROM products ORDER BY price DESC")
        for row in cursor.fetchall():
            print(f"  {row['name']:15s} {row['price']:>10.2f} PLN  (szt: {row['quantity']})")

        # Agregacja
        cursor.execute("SELECT COUNT(*) as cnt, AVG(price) as avg_price FROM products")
        stats = cursor.fetchone()
        print(f"\nStatystyki: {stats['cnt']} produktow, srednia cena: {stats['avg_price']:.2f} PLN")

        # Filtrowanie
        cursor.execute("SELECT name, price FROM products WHERE price > ?", (300,))
        expensive = cursor.fetchall()
        print(f"\nProdukty > 300 PLN: {[r['name'] for r in expensive]}")

    # Baza znika po zakonczeniu - istniala tylko w RAM
    print("\nBaza w pamieci usunieta (koniec bloku with).")


def demo_closing() -> None:
    """Demonstracja contextlib.closing z sqlite3."""
    print("\n=== contextlib.closing ===")

    # closing() gwarantuje wywolanie .close() po wyjsciu z bloku
    with closing(sqlite3.connect(":memory:")) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT sqlite_version()")
        version = cursor.fetchone()
        print(f"SQLite version: {version[0]}")
        print("Polaczenie zostanie zamkniete automatycznie przez closing().")

    print("Polaczenie zamkniete.")


if __name__ == "__main__":
    demo_memory_database()
    demo_closing()
