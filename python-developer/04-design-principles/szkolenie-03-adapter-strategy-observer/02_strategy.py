"""
Strategy - algorytmy sortowania.

Wzorzec Strategy pozwala zdefiniować rodzinę algorytmów,
zamknąć każdy z nich w osobnej klasie i sprawić, by były wymienne.
Klient może dynamicznie zmieniać algorytm (strategię) w trakcie
działania programu.
"""

from abc import ABC, abstractmethod


class SortStrategy(ABC):
    """Interfejs strategii sortowania"""

    @abstractmethod
    def sort(self, data: list) -> list:
        pass


class BubbleSort(SortStrategy):
    def sort(self, data: list) -> list:
        print("Sortowanie bąbelkowe (małe zbiory)")
        arr = data.copy()
        for i in range(len(arr)):
            for j in range(len(arr) - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr


class QuickSort(SortStrategy):
    def sort(self, data: list) -> list:
        print("Sortowanie szybkie (duże zbiory)")
        if len(data) <= 1:
            return data
        pivot = data[0]
        left = [x for x in data[1:] if x <= pivot]
        right = [x for x in data[1:] if x > pivot]
        return self.sort(left) + [pivot] + self.sort(right)


class Sorter:
    """Kontekst - korzysta ze strategii"""

    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        """Zmiana strategii w runtime!"""
        self._strategy = strategy

    def sort(self, data: list) -> list:
        return self._strategy.sort(data)


# Użycie
if __name__ == "__main__":
    data = [64, 34, 25, 12, 22, 11, 90]

    sorter = Sorter(BubbleSort())
    print(sorter.sort(data))

    # Zmiana strategii w trakcie działania programu
    sorter.set_strategy(QuickSort())
    print(sorter.sort(data))
