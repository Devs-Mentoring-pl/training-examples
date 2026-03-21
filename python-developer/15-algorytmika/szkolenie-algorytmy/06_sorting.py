"""
Algorytmika - Szkolenie 4
Algorytmy sortowania - Bubble Sort, Insertion Sort, Merge Sort, Quick Sort.
"""


# --- Bubble Sort O(n^2) ---
def bubble_sort(data: list) -> list:
    n = len(data)

    for i in range(n - 1):
        swapped = False  # optymalizacja

        for j in range(n - 1 - i):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True

        if not swapped:
            break  # tablica juz posortowana

    return data


# --- Insertion Sort O(n^2) ---
def insertion_sort(data: list) -> list:
    for i in range(1, len(data)):
        key = data[i]  # element do wstawienia
        j = i - 1

        # przesuwamy elementy wieksze od key w prawo
        while j >= 0 and data[j] > key:
            data[j + 1] = data[j]
            j -= 1

        data[j + 1] = key  # wstawiamy element we wlasciwe miejsce

    return data


# --- Merge Sort O(n log n) ---
def merge_sort(data: list) -> list:
    # Warunek bazowy - tablica 0- lub 1-elementowa jest posortowana
    if len(data) <= 1:
        return data

    # Dzielimy tablice na dwie polowy
    mid = len(data) // 2
    left_half = merge_sort(data[:mid])
    right_half = merge_sort(data[mid:])

    # Scalamy posortowane polowy
    return merge(left_half, right_half)


def merge(left: list, right: list) -> list:
    """Scala dwie posortowane listy w jedna posortowana liste."""
    result = []
    i = 0  # indeks lewej polowy
    j = 0  # indeks prawej polowy

    # Porownujemy elementy z obu list i dodajemy mniejszy
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # <= zapewnia stabilnosc sortowania
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Dopisujemy pozostale elementy
    result.extend(left[i:])
    result.extend(right[j:])

    return result


# --- Quick Sort O(n log n) srednio ---
def partition(data: list, low: int, high: int) -> int:
    """Partycjonuje tablice wokol pivota i zwraca indeks podzialu."""
    pivot = data[(low + high) // 2]  # pivot na srodku
    i = low
    j = high

    while i <= j:
        # szukamy elementu >= pivot z lewej strony
        while data[i] < pivot:
            i += 1
        # szukamy elementu <= pivot z prawej strony
        while data[j] > pivot:
            j -= 1

        if i <= j:
            data[i], data[j] = data[j], data[i]  # zamieniamy elementy
            i += 1
            j -= 1

    return i  # zwracamy punkt podzialu


def quick_sort(data: list, low: int = 0, high: int = None) -> list:
    """Sortuje tablice algorytmem Quick Sort."""
    if high is None:
        high = len(data) - 1

    if low < high:
        pivot_index = partition(data, low, high)

        # rekurencyjne sortowanie lewej i prawej czesci
        quick_sort(data, low, pivot_index - 1)
        quick_sort(data, pivot_index, high)

    return data


# --- Testy ---
print("Bubble Sort:", bubble_sort([4, 2, 5, 1, 7]))
# [1, 2, 4, 5, 7]

print("Insertion Sort:", insertion_sort([5, 3, 4, 1, 2]))
# [1, 2, 3, 4, 5]

print("Merge Sort:", merge_sort([8, 3, 5, 1, 4, 2, 6, 7]))
# [1, 2, 3, 4, 5, 6, 7, 8]

print("Quick Sort:", quick_sort([2, 9, 5, 2, 0, 1, 4, 3]))
# [0, 1, 2, 2, 3, 4, 5, 9]
