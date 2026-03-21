"""
Algorytmika - Szkolenie 3
Liczby pierwsze - sprawdzanie pierwszosci O(sqrt(n)) i Sito Eratostenesa.
"""

import math


# --- Sprawdzanie pierwszosci - O(sqrt(n)) ---
def is_prime(n):
    """Sprawdza, czy n jest liczba pierwsza - podejscie O(sqrt(n))."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, math.isqrt(n) + 1, 2):
        if n % i == 0:
            return False
    return True


# --- Sito Eratostenesa ---
def sieve_of_eratosthenes(n):
    """Sito Eratostenesa - wyznacza wszystkie liczby pierwsze do n."""
    if n < 2:
        return []

    # Tablica: is_prime_arr[i] == True oznacza, ze i jest potencjalnie pierwsza
    is_prime_arr = [True] * (n + 1)
    is_prime_arr[0] = False
    is_prime_arr[1] = False

    # Wykreslamy wielokrotnosci kolejnych liczb
    for i in range(2, int(n**0.5) + 1):
        if is_prime_arr[i]:
            # Zaczynamy od i*i, bo mniejsze wielokrotnosci juz wykreslone
            for j in range(i * i, n + 1, i):
                is_prime_arr[j] = False

    # Zbieramy liczby pierwsze
    primes = [i for i in range(2, n + 1) if is_prime_arr[i]]
    return primes


# --- Wyznaczanie dzielnikow O(sqrt(n)) ---
def find_divisors_optimized(n):
    """Wyznacza wszystkie dzielniki liczby n - wersja O(sqrt(n))."""
    divisors = []
    for i in range(1, int(math.isqrt(n)) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:  # unikamy duplikatu (np. sqrt(25) = 5)
                divisors.append(n // i)
    return sorted(divisors)


print(f"is_prime(7) = {is_prime(7)}")       # True
print(f"is_prime(15) = {is_prime(15)}")     # False
print(f"is_prime(97) = {is_prime(97)}")     # True

print(f"\nLiczby pierwsze do 30: {sieve_of_eratosthenes(30)}")
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

print(f"Liczb pierwszych do 1000: {len(sieve_of_eratosthenes(1000))}")
# 168

print(f"\nDzielniki 36: {find_divisors_optimized(36)}")
# [1, 2, 3, 4, 6, 9, 12, 18, 36]
