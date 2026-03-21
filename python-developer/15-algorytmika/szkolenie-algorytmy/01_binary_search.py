"""
Algorytmika - Szkolenie 1
Wyszukiwanie binarne - iteracyjna implementacja O(log n).
"""


def binary_search(values: list[int], target: int) -> int:
    """
    Wyszukiwanie binarne - zwraca indeks szukanego elementu
    lub -1, jesli element nie istnieje w liscie.
    Wymaga posortowanej listy!
    """
    left = 0
    right = len(values) - 1

    while left <= right:
        mid = (left + right) // 2  # wyznaczamy srodek zakresu

        if values[mid] == target:
            return mid               # znalezlismy szukana wartosc!
        elif values[mid] < target:
            left = mid + 1           # szukana wartosc jest w prawej polowie
        else:
            right = mid - 1          # szukana wartosc jest w lewej polowie

    return -1  # wartosc nie istnieje w liscie


# Testowanie
numbers = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]

print(binary_search(numbers, 23))   # Wynik: 5
print(binary_search(numbers, 72))   # Wynik: 8
print(binary_search(numbers, 99))   # Wynik: -1
