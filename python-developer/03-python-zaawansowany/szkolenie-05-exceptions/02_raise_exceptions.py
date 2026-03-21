"""
Szkolenie 5 Exceptions - Przyklad 2
Reczne rzucanie wyjatkow - raise.
"""


# Podejscie bez raise - zwracanie "magicznej wartosci" -1
def mul_positive_nums_bad(*args):
    """Iloczyn liczb dodatnich (zly wzorzec - zwraca -1 jako blad)."""
    result = 1
    for num in args:
        if num <= 0:
            print("Kazda liczba musi byc dodatnia!")
            return -1
        else:
            result *= num
    return result


# Podejscie z raise - pythoniczny sposob
def mul_positive_nums(*args):
    """Iloczyn liczb dodatnich (dobry wzorzec - rzuca wyjatek)."""
    result = 1
    for num in args:
        if num <= 0:
            raise ValueError(f"Only positive numbers! Got: {num}")
        result *= num
    return result


print("=== Podejscie bez raise (zle) ===")
print(f"Wynik: {mul_positive_nums_bad(1, 2, 10, 20, -1)}")
print(f"Wynik: {mul_positive_nums_bad(5, 5, 5, 10)}")


print("\n=== Podejscie z raise (dobrze) ===")
try:
    print(f"Wynik: {mul_positive_nums(1, 2, 10, 20, -1)}")
except ValueError as e:
    print(f"Blad: {e}")

try:
    print(f"Wynik: {mul_positive_nums(5, 5, 5, 10)}")
except ValueError as e:
    print(f"Blad: {e}")
