"""
Szkolenie 3 SQLite3 w Pythonie - Przyklad 2
Dodawanie rekordow (placeholdery), executemany(), pobieranie danych.
"""

import sqlite3
from pathlib import Path

DB_PATH: Path = Path("example_database.sqlite3")


def setup_table() -> None:
    """Tworzy tabele jesli nie istnieje."""
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
    connection.commit()
    connection.close()


def add_user(name: str, email: str, age: int) -> None:
    """Dodaje uzytkownika z uzyciem placeholderow (?)."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Bezpieczne - placeholdery chronia przed SQL Injection
    cursor.execute(
        "INSERT OR IGNORE INTO users (name, email, age) VALUES (?, ?, ?)",
        (name, email, age)
    )

    connection.commit()
    print(f"Uzytkownik {name} dodany.")
    connection.close()


def add_multiple_users(users: list[tuple[str, str, int]]) -> None:
    """Dodaje wielu uzytkownikow jednoczesnie (executemany)."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.executemany(
        "INSERT OR IGNORE INTO users (name, email, age) VALUES (?, ?, ?)",
        users
    )

    connection.commit()
    print(f"Dodano {len(users)} uzytkownikow.")
    connection.close()


def get_all_users() -> list[tuple]:
    """Pobiera wszystkich uzytkownikow (fetchall)."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, email, age FROM users")
    users = cursor.fetchall()

    connection.close()
    return users


def get_user_by_id(user_id: int) -> tuple | None:
    """Pobiera uzytkownika po ID (fetchone)."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, email, age FROM users WHERE id = ?",
        (user_id,)  # Uwaga na przecinek - krotka jednoelementowa!
    )
    user = cursor.fetchone()

    connection.close()
    return user


if __name__ == "__main__":
    setup_table()

    # Dodawanie pojedynczych uzytkownikow
    print("=== Dodawanie uzytkownikow ===")
    add_user("Anna Nowak", "anna@example.com", 25)
    add_user("Piotr Wisniewski", "piotr@example.com", 32)

    # Dodawanie wielu naraz
    print("\n=== Dodawanie wielu (executemany) ===")
    new_users = [
        ("Kasia Zielinska", "kasia@example.com", 27),
        ("Tomek Lewandowski", "tomek@example.com", 35),
        ("Ola Dabrowska", "ola@example.com", 22),
        ("Marek Wojcik", "marek@example.com", 40),
    ]
    add_multiple_users(new_users)

    # Pobieranie wszystkich
    print("\n=== Wszyscy uzytkownicy (fetchall) ===")
    for user in get_all_users():
        print(f"  ID: {user[0]}, Imie: {user[1]}, Email: {user[2]}, Wiek: {user[3]}")

    # Pobieranie po ID
    print("\n=== Uzytkownik po ID (fetchone) ===")
    user = get_user_by_id(1)
    if user:
        print(f"  Znaleziono: {user[1]} ({user[2]})")
    else:
        print("  Nie znaleziono.")
