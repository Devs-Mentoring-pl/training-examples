"""
Algorytmika - Szkolenie 2
Rekurencja - potegowanie, silnia, Fibonacci z memoizacja.
"""

from functools import lru_cache


# --- Rekurencyjne potegowanie ---
def calc_power(base, exp):
    if exp == 0:                          # Warunek krancowy
        return 1
    return base * calc_power(base, exp - 1)  # Krok rekurencyjny


# --- Rekurencyjna silnia ---
def calc_fact(value):
    if value <= 1:        # Warunek krancowy
        return 1
    return value * calc_fact(value - 1)  # Krok rekurencyjny


# --- Silnia - rekurencja ogonowa ---
def calc_fact_tail(value, result=1):
    if value <= 1:
        return result                         # Wynik gotowy
    return calc_fact_tail(value - 1, result * value)  # Wynik obliczany na biezaco


# --- Fibonacci z memoizacja ---
@lru_cache(maxsize=None)
def fib(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)


print(f"2^10 = {calc_power(2, 10)}")       # 1024
print(f"5! = {calc_fact(5)}")               # 120
print(f"5! (tail) = {calc_fact_tail(5)}")   # 120
print(f"fib(10) = {fib(10)}")               # 55
print(f"fib(50) = {fib(50)}")               # 12586269025
