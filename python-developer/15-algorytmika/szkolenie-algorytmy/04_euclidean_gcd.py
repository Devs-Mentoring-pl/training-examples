"""
Algorytmika - Szkolenie 2
Algorytm Euklidesa - wyznaczanie NWD (GCD) rekurencyjnie i iteracyjnie.
"""


# --- Wersja rekurencyjna z modulo ---
def calc_gcd(a, b):
    if b == 0:           # Warunek krancowy
        return a
    return calc_gcd(b, a % b)  # Krok rekurencyjny z modulo


# --- Wersja iteracyjna ---
def calc_gcd_iterative(a, b):
    while b != 0:
        a, b = b, a % b
    return a


print(calc_gcd(65, 39))         # Wynik: 13
print(calc_gcd(10, 35))         # Wynik: 5
print(calc_gcd(1000000, 3))     # Wynik: 1

print(calc_gcd_iterative(65, 39))  # Wynik: 13
