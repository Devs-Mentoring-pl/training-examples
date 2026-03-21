"""
Szkolenie 4 Listy skladane i Generatory - Przyklad 5
Laczenie generatorow w pipeline - ciag kwadratow Fibonacciego.
"""


def fibonacci_numbers(nums: int):
    """Generator ciagu Fibonacciego (pierwsze `nums` wyrazow)."""
    x, y = 0, 1
    for _ in range(nums):
        yield x
        x, y = y, x + y


def get_squares(fib_gen):
    """Generator kwadratow wartosci z innego generatora."""
    for num in fib_gen:
        yield num ** 2


def only_even(gen):
    """Generator filtrujacy - przepuszcza tylko parzyste."""
    for num in gen:
        if num % 2 == 0:
            yield num


# Pipeline 1: Kwadraty Fibonacciego
print("=== Pipeline: kwadraty Fibonacciego ===")
print("Ciag Fibonacciego (15 wyrazow):")
for val in fibonacci_numbers(15):
    print(f"  {val}", end="")
print()

print("\nKwadraty Fibonacciego:")
gen = get_squares(fibonacci_numbers(15))
for val in gen:
    print(f"  {val}", end="")
print()


# Pipeline 2: Parzyste Fibonacciego
print("\n=== Pipeline: parzyste Fibonacciego ===")
even_fib = only_even(fibonacci_numbers(20))
print("Parzyste wyrazy ciagu Fibonacciego (z 20 pierwszych):")
for val in even_fib:
    print(f"  {val}", end="")
print()


# Pipeline 3: Kwadraty parzystych Fibonacciego (3 generatory)
print("\n=== Pipeline: kwadraty parzystych Fibonacciego ===")
pipeline = get_squares(only_even(fibonacci_numbers(20)))
print("Kwadraty parzystych Fibonacciego:")
for val in pipeline:
    print(f"  {val}", end="")
print()
