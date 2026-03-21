"""
Szkolenie 8 Type Hints - Przyklad 3
Optional, Union (Python 3.10+ syntax), Callable, TypeVar.
"""

from typing import Callable, TypeVar


# ========== Union (str | int) - Python 3.10+ ==========

def parse_value(value: str | int) -> str:
    """Akceptuje str lub int, zwraca str."""
    return str(value)


def find_index(items: list[str], target: str) -> int | None:
    """Zwraca indeks lub None jesli nie znaleziono."""
    try:
        return items.index(target)
    except ValueError:
        return None


print("=== Union: str | int ===")
print(f"parse_value(42) = '{parse_value(42)}'")
print(f"parse_value('hello') = '{parse_value('hello')}'")

print("\n=== Optional: int | None ===")
fruits = ["apple", "banana", "cherry"]
print(f"find_index(fruits, 'banana') = {find_index(fruits, 'banana')}")
print(f"find_index(fruits, 'mango') = {find_index(fruits, 'mango')}")


# ========== Callable - typy funkcji ==========

def apply_operation(a: int, b: int, operation: Callable[[int, int], int]) -> int:
    """Funkcja przyjmujaca inna funkcje jako argument."""
    return operation(a, b)


print("\n=== Callable ===")
print(f"add: {apply_operation(10, 3, lambda a, b: a + b)}")
print(f"mul: {apply_operation(10, 3, lambda a, b: a * b)}")
print(f"pow: {apply_operation(2, 8, lambda a, b: a ** b)}")


# ========== TypeVar - typy generyczne ==========

T = TypeVar("T")


def first_element(items: list[T]) -> T:
    """Zwraca pierwszy element listy - zachowuje typ."""
    return items[0]


print("\n=== TypeVar ===")
name = first_element(["Anna", "Bartek"])    # typ: str
number = first_element([1, 2, 3])           # typ: int
print(f"first_element(['Anna', 'Bartek']) = '{name}'")
print(f"first_element([1, 2, 3]) = {number}")


# TypeVar z ograniczeniem
Number = TypeVar("Number", int, float)


def double(value: Number) -> Number:
    return value * 2


print(f"\ndouble(5) = {double(5)}")
print(f"double(3.14) = {double(3.14)}")


# ========== Praktyczny przyklad ==========

def find_user(user_id: int) -> dict[str, str] | None:
    """Zwraca dane uzytkownika lub None."""
    users = {1: {"name": "Anna"}, 2: {"name": "Bartek"}}
    return users.get(user_id)


print("\n=== Praktyczny przyklad ===")
user = find_user(1)
if user:
    print(f"Znaleziono: {user['name']}")
else:
    print("Nie znaleziono")

user = find_user(99)
if user:
    print(f"Znaleziono: {user['name']}")
else:
    print("Nie znaleziono uzytkownika o ID 99")
