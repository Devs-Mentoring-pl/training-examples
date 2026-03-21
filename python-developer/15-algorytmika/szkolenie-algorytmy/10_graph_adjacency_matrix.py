"""
Algorytmika - Szkolenie 6
Graf - implementacja macierza sasiedztwa.
"""

from typing import List


class Graph:
    """Graf implementowany za pomoca macierzy sasiedztwa."""

    def __init__(self) -> None:
        self.matrix: List[List[int]] = []
        self.no_vertices: int = 0

    def add_vertex(self) -> None:
        """Dodaje nowy wierzcholek - rozszerza macierz o wiersz i kolumne."""
        self.no_vertices += 1

        # Dodajemy nowa kolumne do kazdego istniejacego wiersza
        for row in self.matrix:
            row.append(0)

        # Dodajemy nowy wiersz (caly wypelniony zerami)
        self.matrix.append([0] * self.no_vertices)

    def get_neighbours(self, id: int) -> List[int]:
        """Zwraca caly wiersz macierzy dla danego wierzcholka."""
        return self.matrix[id]

    def add_edge(self, start: int, end: int, weight: int) -> None:
        """Dodaje krawedz skierowana z waga."""
        self.matrix[start][end] = weight

    def show_graph(self) -> None:
        """Wyswietla graf w czytelnej formie."""
        for id, row in enumerate(self.matrix):
            connected = [
                str(nbr_id) for nbr_id, weight in enumerate(row)
                if weight != 0
            ]
            print(f"{id} połączony z: {', '.join(connected)}")

    def show_matrix(self) -> None:
        """Wyswietla macierz sasiedztwa."""
        # Naglowek
        header = "     " + "  ".join(f"{i:3}" for i in range(self.no_vertices))
        print(header)
        print("   " + "─" * (len(header) - 2))
        # Wiersze
        for i, row in enumerate(self.matrix):
            values = "  ".join(f"{v:3}" for v in row)
            print(f" {i} │ {values}")


# --- Budujemy graf ---
g = Graph()

for i in range(6):
    g.add_vertex()

g.add_edge(0, 2, 1)
g.add_edge(0, 5, 6)
g.add_edge(0, 4, 5)
g.add_edge(1, 4, 10)
g.add_edge(1, 5, 8)
g.add_edge(2, 3, 5)
g.add_edge(2, 0, 1)
g.add_edge(3, 2, 5)
g.add_edge(4, 2, 3)
g.add_edge(4, 0, 5)
g.add_edge(4, 5, 2)
g.add_edge(4, 1, 10)
g.add_edge(5, 0, 6)
g.add_edge(5, 1, 8)
g.add_edge(5, 4, 2)

g.show_graph()
print()
g.show_matrix()
