"""
Szkolenie 3 SQLite3 w Pythonie - Przyklad 1
Tworzenie bazy danych, kursora, tabeli.
"""

import sqlite3
from pathlib import Path

DB_PATH: Path = Path("example_database.sqlite3")


def create_database() -> None:
    """Tworzy baze danych i sprawdza wersje SQLite."""
    connection: sqlite3.Connection = sqlite3.connect(DB_PATH)
    cursor: sqlite3.Cursor = connection.cursor()

    # Sprawdzenie wersji SQLite
    cursor.execute("SELECT sqlite_version()")
    version: tuple = cursor.fetchone()
    print(f"Wersja SQLite: {version[0]}")

    connection.close()
    print(f"Polaczono i zamknieto baze: {DB_PATH}")


def create_table() -> None:
    """Tworzy tabele users w bazie danych."""
    connection: sqlite3.Connection = sqlite3.connect(DB_PATH)
    cursor: sqlite3.Cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER
        )
    """)

    connection.commit()
    print("Tabela 'users' utworzona.")
    connection.close()


if __name__ == "__main__":
    create_database()
    create_table()
