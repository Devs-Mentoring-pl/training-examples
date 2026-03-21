"""
Algorytmika - Szkolenie 1
Gra w zgadywanie - wyszukiwanie binarne w praktyce.
"""

import random


def guessing_game() -> None:
    """Gra w zgadywanie z wykorzystaniem wyszukiwania binarnego."""
    secret = random.randint(1, 1000)
    left, right = 1, 1000
    attempts = 0

    print("Pomyślałem liczbę od 1 do 1000. Komputer spróbuje ją zgadnąć!")
    print(f"(Podpowiedź: to {secret})\n")

    while left <= right:
        mid = (left + right) // 2
        attempts += 1
        print(f"Próba {attempts}: Czy to {mid}?", end=" ")

        if mid == secret:
            print(f"→ TAK! Odgadnięto w {attempts} próbach!")
            return
        elif mid < secret:
            print("→ Za mało, szukam wyżej")
            left = mid + 1
        else:
            print("→ Za dużo, szukam niżej")
            right = mid - 1


guessing_game()
