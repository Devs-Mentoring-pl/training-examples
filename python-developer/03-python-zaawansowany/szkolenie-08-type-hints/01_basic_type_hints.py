"""
Szkolenie 8 Type Hints - Przyklad 1
Podstawowa skladnia type hints - zmienne, argumenty, wartosci zwracane.
"""


# Typowanie zmiennych
name: str = "Kacper"
age: int = 25
salary: float = 8500.50
is_active: bool = True

print("=== Typowane zmienne ===")
print(f"name: {name} (typ: {type(name).__name__})")
print(f"age: {age} (typ: {type(age).__name__})")
print(f"salary: {salary} (typ: {type(salary).__name__})")
print(f"is_active: {is_active} (typ: {type(is_active).__name__})")


# Typowanie argumentow i wartosci zwracanej
def greet(name: str) -> str:
    return f"Czesc, {name}!"


def add(a: int, b: int) -> int:
    return a + b


def is_adult(age: int) -> bool:
    return age >= 18


def log_message(message: str) -> None:
    print(f"[LOG] {message}")


print("\n=== Typowane funkcje ===")
print(greet("Anna"))
print(f"add(3, 5) = {add(3, 5)}")
print(f"is_adult(25) = {is_adult(25)}")
print(f"is_adult(15) = {is_adult(15)}")
log_message("Operacja zakonczona")


# Argumenty domyslne z typami
def create_user(name: str, role: str = "user", active: bool = True) -> dict:
    return {"name": name, "role": role, "active": active}


print("\n=== Argumenty domyslne ===")
print(create_user("Jan"))
print(create_user("Anna", role="admin"))


# Porownanie z typami vs bez
def calculate_discount(price: float, discount: float) -> float:
    """Od razu widac: float wchodzi, float wychodzi."""
    return price * (1 - discount)


print("\n=== Kalkulator znizek ===")
print(f"Cena 100 ze znizka 20%: {calculate_discount(100.0, 0.2)}")
