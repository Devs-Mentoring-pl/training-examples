"""
Szkolenie 5 Exceptions - Przyklad 1
Blok try/except - podstawowa obsluga wyjatkow.
"""


# Przyklad 1: Dzielenie z obsluga bledu
print("=== try/except: dzielenie ===")

a = 10
b = 0

try:
    result = a / b
    print(f"Wynik: {result}")
except ZeroDivisionError:
    print("Nie mozna dzielic przez 0!")


# Przyklad 2: Dzielenie przez elementy listy - rozne typy bledow
print("\n=== try/except: rozne typy wyjatkow ===")
values = ['a', 0, 2, 3.5]

for elem in values:
    try:
        print(f"Element: {elem}", end=" -> ")
        r = 1 / elem
        print(f"Wynik: {r}")
    except ZeroDivisionError:
        print("Nie mozna dzielic przez 0!")
    except TypeError:
        print("Nie mozna dzielic przez litere!")


# Przyklad 3: Najczestsze wyjatki
print("\n=== Przyklady najczestszych wyjatkow ===")

# TypeError
try:
    result = "tekst" + 5
except TypeError as e:
    print(f"TypeError: {e}")

# IndexError
try:
    my_list = [1, 2, 3]
    print(my_list[100])
except IndexError as e:
    print(f"IndexError: {e}")

# ValueError
try:
    number = int("abc")
except ValueError as e:
    print(f"ValueError: {e}")

# KeyError
try:
    d = {"a": 1}
    print(d["b"])
except KeyError as e:
    print(f"KeyError: {e}")
