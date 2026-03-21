"""
Szkolenie 3 Programowanie funkcyjne - Przyklad 2
Lambda jako argument funkcji higher order.
"""


def calc_result(x, y, op):
    """Funkcja higher order - przyjmuje inna funkcje jako argument."""
    print("Hi!")
    print("I am starting the computation process...")
    return op(x, y)


# Potegowanie
print("=== Potegowanie ===")
print(f"Wynik: {calc_result(1, 2, lambda x, y: x**y)}")

# Dodawanie
print("\n=== Dodawanie ===")
print(f"Wynik: {calc_result(1, 2, lambda x, y: x + y)}")

# Dzielenie calkowite
print("\n=== Dzielenie calkowite ===")
print(f"Wynik: {calc_result(1, 2, lambda x, y: x // y)}")

# Mnozenie
print("\n=== Mnozenie ===")
print(f"Wynik: {calc_result(3, 4, lambda x, y: x * y)}")
