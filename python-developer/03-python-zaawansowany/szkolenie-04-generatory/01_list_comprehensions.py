"""
Szkolenie 4 Listy skladane i Generatory - Przyklad 1
Listy skladane (list comprehensions) - zwiezly sposob tworzenia list.
"""


# Przyklad 1: N kolejnych kwadratow liczb naturalnych
print("=== Kwadraty liczb: petla vs list comprehension ===")
N = 10

# Podejscie z petla for
quadratics_loop = []
for i in range(N):
    quadratics_loop.append(i**2)

# Podejscie z lista skladana
quadratics_comp = [i**2 for i in range(N)]

print(f"Petla for:        {quadratics_loop}")
print(f"Comprehension:    {quadratics_comp}")
print(f"Identyczne: {quadratics_loop == quadratics_comp}")


# Przyklad 2: Co drugi znak ze zdania
print("\n=== Co drugi znak ze zdania ===")
txt = "Lezy Jerzy na wiezy i nie wierzy, ze na drugiej wiezy lezy drugi Jerzy."
filtered_ltrs = [txt[i] for i in range(0, len(txt), 2)]
print(filtered_ltrs)


# Przyklad 3: Lista skladana z warunkiem - dozwolone wyrazy
print("\n=== Dozwolone wyrazy ===")
allowed_words = ['w', 'pod', 'i', 'nad', 'o']
txt2 = "Ala i Stas trzymaja koty w piwnicy pod kuchnia o swicie"
found_words = [word for word in txt2.split() if word in allowed_words]
print(found_words)  # ['i', 'w', 'pod', 'o']


# Przyklad 4: Kwadraty tylko liczb parzystych - comprehension vs map+filter
print("\n=== Kwadraty parzystych: comprehension vs map+filter ===")

# List comprehension - czytelne
squares_even = [i**2 for i in range(10) if not i % 2]

# map + filter + lambda - mniej czytelne
squares_even_func = list(map(lambda x: x**2, filter(lambda x: not x % 2, range(10))))

print(f"Comprehension: {squares_even}")
print(f"map+filter:    {squares_even_func}")


# Przyklad 5: Splaszczenie macierzy
print("\n=== Splaszczenie macierzy 2D ===")
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flatten = [x for row in matrix for x in row]
print(f"Macierz: {matrix}")
print(f"Flat:    {flatten}")
