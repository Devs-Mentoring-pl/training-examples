"""
Szkolenie 3 Programowanie funkcyjne - Przyklad 5
reduce() - redukowanie sekwencji do pojedynczej wartosci.
"""

from functools import reduce


# Przyklad 1: Suma elementow (wlasna implementacja sum())
print("=== reduce: suma ===")
nums = [1, 2, 3, 4, 30]
result = reduce(lambda x, y: x + y, nums)
print(f"Suma {nums} = {result}")  # 40

# Krok po kroku:
# 1 + 2 = 3
# 3 + 3 = 6
# 6 + 4 = 10
# 10 + 30 = 40


# Przyklad 1.1: Suma z argumentem initial
print("\n=== reduce: suma z initial=10 ===")
result_with_initial = reduce(lambda x, y: x + y, nums, 10)
print(f"Suma {nums} (start od 10) = {result_with_initial}")  # 50

# Krok po kroku:
# start: 10
# 10 + 1 = 11
# 11 + 2 = 13
# 13 + 3 = 16
# 16 + 4 = 20
# 20 + 30 = 50


# Przyklad 2: Iloczyn elementow
print("\n=== reduce: iloczyn ===")
nums2 = [2, 2, 2, 2, 10]
product = reduce(lambda x, y: x * y, nums2)
print(f"Iloczyn {nums2} = {product}")  # 160


# Przyklad 3: Znajdowanie najdluzszego stringa
print("\n=== reduce: najdluzszy string ===")
words = ["Python", "programowanie", "funkcyjne", "jest", "super"]
longest = reduce(lambda x, y: x if len(x) >= len(y) else y, words)
print(f"Najdluzszy wyraz: '{longest}'")  # 'programowanie'


# Przyklad 4: Zliczanie wystapien
print("\n=== reduce: zliczanie wystapien ===")
data = ['a', 'b', 'a', 'c', 'b', 'a', 'd', 'c', 'a']
counts = reduce(
    lambda acc, item: {**acc, item: acc.get(item, 0) + 1},
    data,
    {}
)
print(f"Dane:       {data}")
print(f"Wystapienia: {counts}")
