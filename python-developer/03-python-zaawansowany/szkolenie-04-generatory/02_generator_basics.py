"""
Szkolenie 4 Listy skladane i Generatory - Przyklad 2
Generatory - funkcje z yield, leniwe iteratory.
"""


def gen_infinite_nums():
    """Generator nieskonczonego ciagu liczb."""
    num = 0
    while True:
        yield num
        num += 1


# Tworzenie generatora i pobieranie wartosci
print("=== Generator nieskonczonego ciagu ===")
generator = gen_infinite_nums()
print(f"next(): {next(generator)}")   # 0
print(f"next(): {next(generator)}")   # 1

print("\nKolejne 10 wartosci (petla for z next):")
for i in range(10):
    print(f"  next(): {next(generator)}")
# Generator pamięta stan - kontynuuje od 2


# Zobrazowanie yield - wiele yield w jednej funkcji
print("\n=== Wiele yield w generatorze ===")


def multi_yield():
    first_yield = "That's the first yield"
    yield first_yield
    second_yield = "That's the second yield"
    yield second_yield


gen = multi_yield()
print(next(gen))   # "That's the first yield"
print(next(gen))   # "That's the second yield"

# Trzecie wywolanie next() spowoduje StopIteration
try:
    print(next(gen))
except StopIteration:
    print("StopIteration - generator wyczerpany!")
