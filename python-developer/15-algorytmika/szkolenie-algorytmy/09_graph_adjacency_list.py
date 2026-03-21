"""
Algorytmika - Szkolenie 6
Graf - implementacja lista sasiedztwa (klasy Vertex i Graph).
"""

from __future__ import annotations
from typing import Dict, Optional, Iterator


class Vertex:
    """Reprezentuje pojedynczy wierzcholek grafu."""

    def __init__(self, id: int) -> None:
        self.__id = id
        self.neighbours: Dict[Vertex, int] = {}

    def add_neighbour(self, new_id: int, weight: int) -> None:
        """Dodaje sasiada o podanym ID z waga krawedzi."""
        self.neighbours[Vertex(new_id)] = weight

    @property
    def id(self) -> int:
        return self.__id

    def get_weight(self, neighbour: Vertex) -> Optional[int]:
        """Zwraca wage krawedzi do podanego sasiada."""
        return self.neighbours.get(neighbour, None)

    def get_neighbours(self) -> list:
        """Zwraca liste sasiednich wierzcholkow."""
        return list(self.neighbours.keys())

    def __str__(self) -> str:
        neighbours_str = ", ".join(
            str(vertex.id) for vertex in self.neighbours
        )
        return f"{self.id} połączony z: {neighbours_str}"


class Graph:
    """Graf implementowany za pomoca listy sasiedztwa."""

    def __init__(self) -> None:
        self.vertices: Dict[int, Vertex] = {}

    def add_vertex(self, new_id: int) -> None:
        """Dodaje nowy wierzcholek do grafu."""
        self.vertices[new_id] = Vertex(new_id)

    def get_vertex(self, id: int) -> Optional[Vertex]:
        """Zwraca wierzcholek o podanym ID."""
        return self.vertices.get(id, None)

    def add_edge(self, first_id: int, second_id: int, weight: int) -> None:
        """Dodaje skierowana krawedz z waga."""
        try:
            self.vertices[first_id].add_neighbour(second_id, weight)
        except KeyError:
            print("Nie znaleziono wierzchołka!")

    def __iter__(self) -> Iterator:
        return iter(self.vertices.values())


# --- Budujemy graf ---
g = Graph()

for i in range(6):
    g.add_vertex(i)

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

for v in g:
    print(v)
