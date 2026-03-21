"""
Szkolenie 3 Programowanie funkcyjne - Przyklad 3
filter() - filtrowanie elementow wedlug warunku w lambdzie.
"""


# Przyklad 1: Liczby wieksze lub rowne 4
print("=== filter: liczby >= 4 ===")
elements = [20, 23, 24, 1, 2, -5, 0, 2, 3, 4]
filtered_result = filter(lambda x: x >= 4, elements)
print(list(filtered_result))  # [20, 23, 24, 4]


# Przyklad 2: Imiona konczace sie na litere 'a'
print("\n=== filter: imiona konczace sie na 'a' ===")
names = {'Kacper', 'Jan', 'Lukasz', 'Elzbieta', 'Joanna', 'Jakub', 'Alicja',
         'Kinga', 'Patrycja'}
result = filter(lambda name: name[-1] == 'a', names)
print(set(result))


# Przyklad 3: Palindromy
print("\n=== filter: palindromy ===")
dromes = ("demigod", "rewire", "madam", "freer", "anutforajaroftuna", "kiosk")
palindromes = list(filter(lambda word: word == word[::-1], dromes))
print(palindromes)  # ['madam', 'anutforajaroftuna']


# Przyklad 4: Liczby parzyste i wieksze od 10
print("\n=== filter: parzyste i > 10 ===")
numbers = [3, 12, 7, 20, 5, 18, 2, 14, 9, 30]
result = list(filter(lambda x: x % 2 == 0 and x > 10, numbers))
print(result)  # [12, 20, 18, 14, 30]
