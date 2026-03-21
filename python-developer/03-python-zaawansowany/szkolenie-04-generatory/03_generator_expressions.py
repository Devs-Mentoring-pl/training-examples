"""
Szkolenie 4 Listy skladane i Generatory - Przyklad 3
Wyrazenia generatorow vs listy skladane - roznice w pamieci i zachowaniu.
"""

import sys


# Porownanie: lista skladana vs wyrazenie generatora
print("=== Lista skladana vs generator ===")
nums_squared_list = [x**2 for x in range(10)]        # lista
nums_squared_gen = (x**2 for x in range(10))          # generator!

print(f"Lista:     {nums_squared_list}")
print(f"Generator: {nums_squared_gen}")
print()

# Odczyt z generatora - konieczne next() lub petla
print("Wartosci z generatora:")
for val in nums_squared_gen:
    print(f"  {val}", end="")
print()


# Porownanie zuzycia pamieci
print("\n=== Porownanie pamieci ===")
big_list = [x**2 for x in range(100_000)]
big_gen = (x**2 for x in range(100_000))

print(f"Rozmiar listy:     {sys.getsizeof(big_list):>10} bajtow")
print(f"Rozmiar generatora:{sys.getsizeof(big_gen):>10} bajtow")


# Praktyczny przyklad - suma z generatorem (bez tworzenia listy)
print("\n=== Suma kwadratow: lista vs generator ===")
# Z lista - tworzy cala liste w pamieci
sum_list = sum([x**2 for x in range(1_000_000)])

# Z generatorem - oblicza leniwie, element po elemencie
sum_gen = sum(x**2 for x in range(1_000_000))

print(f"Suma (lista):     {sum_list}")
print(f"Suma (generator): {sum_gen}")
print(f"Wyniki identyczne: {sum_list == sum_gen}")
