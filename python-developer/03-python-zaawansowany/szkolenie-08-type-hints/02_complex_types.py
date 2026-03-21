"""
Szkolenie 8 Type Hints - Przyklad 2
Typy zlozone: list, dict, tuple, set, zagniezdzone typy.
Wymaga Python 3.9+ (wbudowane typy generyczne).
"""


# Listy
scores: list[int] = [95, 87, 73, 100]
names: list[str] = ["Anna", "Bartek", "Celina"]


def average(numbers: list[float]) -> float:
    return sum(numbers) / len(numbers)


print("=== Listy ===")
print(f"scores: {scores}")
print(f"names: {names}")
print(f"average(scores): {average([float(s) for s in scores]):.2f}")


# Slowniki
word_count: dict[str, int] = {"python": 42, "java": 15}


def get_config() -> dict[str, str]:
    return {"host": "localhost", "port": "5432"}


print("\n=== Slowniki ===")
print(f"word_count: {word_count}")
print(f"config: {get_config()}")


# Krotki
point: tuple[float, float, float] = (1.0, 2.5, 3.7)
tags: tuple[str, ...] = ("python", "typing", "mypy")

print("\n=== Krotki ===")
print(f"point (3 elementy): {point}")
print(f"tags (zmienna dlugosc): {tags}")


# Zbiory
unique_ids: set[int] = {1, 2, 3, 4, 5}


def get_unique_words(text: str) -> set[str]:
    return set(text.lower().split())


print("\n=== Zbiory ===")
print(f"unique_ids: {unique_ids}")
print(f"unique words: {get_unique_words('Python jest super Python jest')}")


# Zagniezdzone typy
users: list[dict[str, str]] = [
    {"name": "Anna", "email": "anna@example.com"},
    {"name": "Bartek", "email": "bartek@example.com"},
]

grades: dict[str, list[int]] = {
    "matematyka": [5, 4, 3],
    "fizyka": [4, 4, 5],
}

print("\n=== Zagniezdzone typy ===")
print(f"users: {users}")
print(f"grades: {grades}")
for subject, grade_list in grades.items():
    avg = sum(grade_list) / len(grade_list)
    print(f"  {subject}: srednia = {avg:.2f}")
