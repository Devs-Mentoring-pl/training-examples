"""
Szkolenie 3 SQLite3 w Pythonie - Przyklad 4
Podejscie obiektowe - klasa Database z context managerem.
"""

import sqlite3
from pathlib import Path


class Database:
    """Klasa obslugujaca polaczenie z baza SQLite z context managerem."""

    def __init__(self, db_path: Path) -> None:
        self.db_path: Path = db_path
        self.connection: sqlite3.Connection | None = None
        self.cursor: sqlite3.Cursor | None = None

    def __enter__(self) -> "Database":
        """Otwiera polaczenie przy wejsciu do bloku with."""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type: type | None, exc_val: Exception | None,
                 exc_tb: object | None) -> None:
        """Zamyka polaczenie przy wyjsciu z bloku with."""
        if exc_type is not None:
            self.connection.rollback()
            print(f"Blad: {exc_val}. Zmiany cofniete (rollback).")
        else:
            self.connection.commit()
        self.connection.close()

    def create_table(self) -> None:
        """Tworzy tabele users."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER
            )
        """)

    def add_user(self, name: str, email: str, age: int) -> None:
        """Dodaje uzytkownika do bazy."""
        self.cursor.execute(
            "INSERT OR IGNORE INTO users (name, email, age) VALUES (?, ?, ?)",
            (name, email, age)
        )

    def get_all_users(self) -> list[sqlite3.Row]:
        """Pobiera wszystkich uzytkownikow."""
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def get_user_by_id(self, user_id: int) -> sqlite3.Row | None:
        """Pobiera uzytkownika po ID."""
        self.cursor.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )
        return self.cursor.fetchone()

    def update_user(self, user_id: int, name: str, email: str, age: int) -> None:
        """Aktualizuje dane uzytkownika."""
        self.cursor.execute(
            "UPDATE users SET name = ?, email = ?, age = ? WHERE id = ?",
            (name, email, age, user_id)
        )

    def delete_user(self, user_id: int) -> bool:
        """Usuwa uzytkownika po ID. Zwraca True jesli usuniety."""
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        return self.cursor.rowcount > 0


if __name__ == "__main__":
    db_path = Path("example_oop.sqlite3")

    # Uzycie z blokiem with - bezpieczne
    print("=== Klasa Database z context managerem ===")

    with Database(db_path) as db:
        db.create_table()

        # Dodawanie uzytkownikow
        db.add_user("Adam Nowicki", "adam@example.com", 33)
        db.add_user("Ewa Kowalska", "ewa@example.com", 29)
        db.add_user("Tomek Zielinski", "tomek@example.com", 45)

        # Wyswietlanie wszystkich
        print("\nWszyscy uzytkownicy:")
        for user in db.get_all_users():
            print(f"  {user['id']}. {user['name']} - {user['email']} (wiek: {user['age']})")

        # Pobieranie po ID
        print("\nUzytkownik ID=1:")
        user = db.get_user_by_id(1)
        if user:
            print(f"  {user['name']} ({user['email']})")

        # Aktualizacja
        db.update_user(1, "Adam Nowicki-Zmieniony", "adam.new@example.com", 34)
        print("\nPo aktualizacji ID=1:")
        user = db.get_user_by_id(1)
        if user:
            print(f"  {user['name']} ({user['email']})")

        # Usuniecie
        deleted = db.delete_user(3)
        print(f"\nUsunieto ID=3: {deleted}")

        print("\nPozostali uzytkownicy:")
        for user in db.get_all_users():
            print(f"  {user['id']}. {user['name']}")

    # Polaczenie jest juz zamkniete - automatycznie!
    print("\nPolaczenie zamkniete automatycznie.")

    # Sprzatanie pliku testowego
    import os
    os.remove(db_path)
    print(f"Plik {db_path} usuniety.")
