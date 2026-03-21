"""
Szkolenie 8 Type Hints - Przyklad 5
Zaawansowane typy: TypedDict, Protocol, Literal, Final.
"""

from typing import TypedDict, Protocol, Literal, Final


# ========== TypedDict - slowniki ze znanymi kluczami ==========

class UserData(TypedDict):
    name: str
    age: int
    email: str | None


def create_user(data: UserData) -> None:
    print(f"  Tworze uzytkownika: {data['name']}, wiek: {data['age']}")


print("=== TypedDict ===")
create_user({"name": "Anna", "age": 25, "email": "anna@example.com"})
create_user({"name": "Bartek", "age": 30, "email": None})


# ========== Protocol - duck typing z weryfikacja ==========

class Drawable(Protocol):
    def draw(self) -> None: ...


class Circle:
    def draw(self) -> None:
        print("  Rysuje kolo")


class Square:
    def draw(self) -> None:
        print("  Rysuje kwadrat")


class Triangle:
    def draw(self) -> None:
        print("  Rysuje trojkat")


def render(shape: Drawable) -> None:
    """Akceptuje dowolny obiekt z metoda draw()."""
    shape.draw()


print("\n=== Protocol: duck typing ===")
render(Circle())
render(Square())
render(Triangle())


# ========== Literal - ograniczenie do konkretnych wartosci ==========

def set_direction(direction: Literal["left", "right", "up", "down"]) -> None:
    print(f"  Kierunek: {direction}")


def open_file(path: str, mode: Literal["r", "w", "a"]) -> None:
    print(f"  Otwieram '{path}' w trybie '{mode}'")


print("\n=== Literal ===")
set_direction("left")
set_direction("up")
open_file("data.txt", "r")


# ========== Final - stale ==========

MAX_CONNECTIONS: Final = 100
API_VERSION: Final[str] = "v2"

print("\n=== Final (stale) ===")
print(f"MAX_CONNECTIONS: {MAX_CONNECTIONS}")
print(f"API_VERSION: {API_VERSION}")
# MAX_CONNECTIONS = 200  # mypy zglosi blad!


# ========== Praktyczny przyklad: typowany serwis ==========

class ApiResponse(TypedDict):
    status: int
    data: dict[str, str] | None
    error: str | None


def handle_response(response: ApiResponse) -> None:
    if response["status"] < 400:
        print(f"  Sukces ({response['status']}): {response['data']}")
    else:
        print(f"  Blad ({response['status']}): {response['error']}")


print("\n=== Praktyczny przyklad: ApiResponse ===")
handle_response({"status": 200, "data": {"user": "Anna"}, "error": None})
handle_response({"status": 404, "data": None, "error": "Not found"})
