"""
Szkolenie 5 Exceptions - Przyklad 4
Tworzenie wlasnych wyjatkow - klasy dziedziczace po Exception.
"""


class ValueTooSmallError(Exception):
    """Wyjatek rzucany gdy wartosc jest za mala."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Typed value - {self.value} - is too small!"


class ValueTooBigError(Exception):
    """Wyjatek rzucany gdy wartosc jest za duza."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Typed value - {self.value} - is too big!"


def get_num_in_range(start: int, end: int, value: int) -> int:
    """Sprawdza czy wartosc miesci sie w podanym zakresie."""
    if value < start:
        raise ValueTooSmallError(value)
    elif value > end:
        raise ValueTooBigError(value)
    return value


# Testowanie wlasnych wyjatkow
print("=== Wlasne wyjatki: zakres liczb ===")

test_values = [-1, 2, 10]

for val in test_values:
    try:
        result = get_num_in_range(1, 5, val)
        print(f"  Wartosc {val}: OK -> {result}")
    except (ValueTooSmallError, ValueTooBigError) as e:
        print(f"  Wartosc {val}: BLAD -> {e}")


# Bardziej rozbudowany przyklad - kalkulator z wlasnym wyjatkiem
print("\n=== Wlasne wyjatki: kalkulator ===")


class InvalidOperationError(Exception):
    """Wyjatek rzucany dla nieobslugiwanej operacji."""
    def __init__(self, operation: str):
        self.operation = operation

    def __str__(self):
        return f"Invalid operation: '{self.operation}'. Allowed: +, -, *, /"


def calculate(a: float, b: float, operation: str) -> float:
    """Prosty kalkulator z walidacja operacji."""
    if operation == "+":
        return a + b
    elif operation == "-":
        return a - b
    elif operation == "*":
        return a * b
    elif operation == "/":
        if b == 0:
            raise ZeroDivisionError("Nie mozna dzielic przez 0!")
        return a / b
    else:
        raise InvalidOperationError(operation)


test_cases = [
    (10, 5, "+"),
    (10, 5, "-"),
    (10, 5, "*"),
    (10, 5, "/"),
    (10, 0, "/"),
    (10, 5, "%"),
]

for a, b, op in test_cases:
    try:
        result = calculate(a, b, op)
    except (ZeroDivisionError, InvalidOperationError) as e:
        print(f"  {a} {op} {b} = BLAD: {e}")
    else:
        print(f"  {a} {op} {b} = {result}")
    finally:
        pass  # W produkcji: logowanie, zamykanie zasobow itp.

print("\nKoniec obliczen.")
