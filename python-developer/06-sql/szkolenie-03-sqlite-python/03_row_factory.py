"""
Szkolenie 3 SQLite3 w Pythonie - Przyklad 3
Row factory - wyniki jako slowniki (dostep po nazwie kolumny).
"""

import sqlite3
from pathlib import Path

DB_PATH: Path = Path("example_database.sqlite3")


def setup_and_populate() -> None:
    """Tworzy tabele i dodaje dane testowe."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER
        )
    """)

    test_users = [
        ("Anna Nowak", "anna@example.com", 25),
        ("Jan Kowalski", "jan@example.com", 30),
        ("Ewa Wisniewska", "ewa@example.com", 28),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO users (name, email, age) VALUES (?, ?, ?)",
        test_users
    )

    connection.commit()
    connection.close()


def get_users_as_tuples() -> None:
    """Pobiera uzytkownikow jako krotki (domyslnie)."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, email, age FROM users")
    users = cursor.fetchall()

    print("=== Krotki (domyslnie) ===")
    for user in users:
        # Dostep po indeksie - mniej czytelne
        print(f"  user[0]={user[0]}, user[1]={user[1]}, user[2]={user[2]}")

    connection.close()


def get_users_as_rows() -> None:
    """Pobiera uzytkownikow jako Row (dostep po nazwie kolumny)."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row   # Ustawienie PRZED kursorem
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, email, age FROM users")
    users = cursor.fetchall()

    print("\n=== sqlite3.Row (po nazwie kolumny) ===")
    for user in users:
        # Dostep po nazwie - czytelne
        print(f"  name={user['name']}, email={user['email']}, age={user['age']}")

    connection.close()


if __name__ == "__main__":
    setup_and_populate()
    get_users_as_tuples()
    get_users_as_rows()
