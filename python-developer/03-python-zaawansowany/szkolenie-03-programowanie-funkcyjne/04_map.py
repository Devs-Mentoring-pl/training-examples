"""
Szkolenie 3 Programowanie funkcyjne - Przyklad 4
map() - stosowanie funkcji do kazdego elementu iterables.
"""


# Przyklad 1: Zamiana liter na wielkie - podejscie imperatywne vs map()
print("=== map: upper() ===")
my_names = ['Elizabeth', 'Sabrina', 'Marry']

# Imperatywne podejscie
uppered_imperative = []
for name in my_names:
    uppered_imperative.append(name.upper())

# Funkcyjne podejscie z map()
uppered_functional = list(map(lambda x: x.upper(), my_names))

print(f"Imperatywne: {uppered_imperative}")
print(f"Funkcyjne:   {uppered_functional}")


# Przyklad 2: Zaokraglanie wartosci - wiele iterables
print("\n=== map: round() z wieloma iterables ===")
areas = [3.12345678, 1.12345678, 10.12345678, 100.12345678, 0.12345678,
         5.12345678, 3.12345678]
rounded_areas = list(map(round, areas, range(1, 8)))
print(rounded_areas)
# [3.1, 1.12, 10.123, 100.1235, 0.12346, 5.123457, 3.1234568]


# Przyklad 2.1: Rozne dlugosci iterables
print("\n=== map: rozne dlugosci iterables ===")
rounded_short = list(map(round, areas, range(1, 3)))
print(rounded_short)  # [3.1, 1.12] - krotsza sekwencja decyduje


# Przyklad 3: Wlasna implementacja zip() za pomoca map()
print("\n=== map: wlasna implementacja zip() ===")
chars = ['a', 'b', 'c', 'd', 'e']
nums = [1, 2, 3, 4, 5]

result_zip = list(zip(chars, nums))
my_result = list(map(lambda x, y: (x, y), chars, nums))

print(f"zip():     {result_zip}")
print(f"map():     {my_result}")
print(f"Identyczne: {result_zip == my_result}")


# Przyklad 4: Konwersja Celsjuszy na Fahrenheity
print("\n=== map: Celsjusze -> Fahrenheity ===")
celsius = [0, 20, 37, 100]
fahrenheit = list(map(lambda c: c * 9/5 + 32, celsius))
for c, f in zip(celsius, fahrenheit):
    print(f"  {c}°C = {f}°F")
