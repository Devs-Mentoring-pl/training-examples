"""
Algorytmika - Szkolenie 7
DFS (przeszukiwanie w glab) i BFS (przeszukiwanie wszerz).
"""

from collections import deque


# --- DFS iteracyjny (stos) ---
def dfs_iterative(graph: dict[int, list[int]], start: int) -> list[int]:
    """Przeszukiwanie w glab - wersja iteracyjna ze stosem."""
    visited = set()
    stack = [start]
    order = []  # kolejnosc odwiedzania

    while stack:
        vertex = stack.pop()  # zdejmij ze szczytu stosu (LIFO)

        if vertex in visited:
            continue

        visited.add(vertex)
        order.append(vertex)

        # Dodaj nieodwiedzonych sasiadow na stos
        for neighbour in graph[vertex]:
            if neighbour not in visited:
                stack.append(neighbour)

    return order


# --- DFS rekurencyjny ---
def dfs_recursive(
    graph: dict[int, list[int]],
    vertex: int,
    visited: set[int] | None = None,
) -> list[int]:
    """Przeszukiwanie w glab - wersja rekurencyjna."""
    if visited is None:
        visited = set()

    visited.add(vertex)
    order = [vertex]

    for neighbour in graph[vertex]:
        if neighbour not in visited:
            order.extend(dfs_recursive(graph, neighbour, visited))

    return order


# --- BFS (kolejka) ---
def bfs(graph: dict[int, list[int]], start: int) -> list[int]:
    """Przeszukiwanie wszerz - z uzyciem collections.deque."""
    visited = set()
    queue = deque([start])  # kolejka FIFO
    order = []

    while queue:
        vertex = queue.popleft()  # pobierz z poczatku kolejki (FIFO)

        if vertex in visited:
            continue

        visited.add(vertex)
        order.append(vertex)

        # Dodaj nieodwiedzonych sasiadow na koniec kolejki
        for neighbour in graph[vertex]:
            if neighbour not in visited:
                queue.append(neighbour)

    return order


# --- BFS najkrotsza sciezka ---
def bfs_shortest_path(
    graph: dict[int, list[int]], start: int, end: int
) -> list[int] | None:
    """Znajdz najkrotsza sciezke w grafie niewazonym (BFS)."""
    visited = set()
    queue = deque([(start, [start])])  # (wierzcholek, sciezka do niego)

    while queue:
        vertex, path = queue.popleft()

        if vertex == end:
            return path  # znalezlismy najkrotsza sciezke!

        if vertex in visited:
            continue

        visited.add(vertex)

        for neighbour in graph[vertex]:
            if neighbour not in visited:
                queue.append((neighbour, path + [neighbour]))

    return None  # brak sciezki


# --- DFS wykrywanie cykli ---
def has_cycle(graph: dict[int, list[int]]) -> bool:
    """Sprawdz, czy graf skierowany zawiera cykl (DFS)."""
    visited = set()
    in_current_path = set()  # wierzcholki w biezacej sciezce rekurencji

    def _dfs(vertex: int) -> bool:
        visited.add(vertex)
        in_current_path.add(vertex)

        for neighbour in graph[vertex]:
            if neighbour in in_current_path:
                return True  # cykl wykryty!
            if neighbour not in visited:
                if _dfs(neighbour):
                    return True

        in_current_path.remove(vertex)  # wycofujemy sie z biezacej sciezki
        return False

    # Sprawdz wszystkie wierzcholki (graf moze nie byc spojny)
    for vertex in graph:
        if vertex not in visited:
            if _dfs(vertex):
                return True

    return False


# --- Sortowanie topologiczne ---
def topological_sort(graph: dict[int, list[int]]) -> list[int]:
    """Sortowanie topologiczne grafu DAG (DFS)."""
    visited = set()
    result = []  # stos wynikowy

    def _dfs(vertex: int) -> None:
        visited.add(vertex)
        for neighbour in graph[vertex]:
            if neighbour not in visited:
                _dfs(neighbour)
        result.append(vertex)  # dodaj PO przetworzeniu wszystkich nastepnikow

    for vertex in graph:
        if vertex not in visited:
            _dfs(vertex)

    return result[::-1]  # odwroc - bo dodawalismy na koniec


# --- Testy ---
graph = {
    0: [4, 5, 2],
    1: [4, 5],
    2: [3, 0],
    3: [2],
    4: [2, 0, 5, 1],
    5: [0, 1, 4],
}

print(f"DFS iteracyjny: {dfs_iterative(graph, start=0)}")
print(f"DFS rekurencyjny: {dfs_recursive(graph, vertex=0)}")
print(f"BFS: {bfs(graph, start=0)}")

# BFS najkrotsza sciezka
path_graph = {
    0: [1, 2],
    1: [0, 3],
    2: [0, 3, 4],
    3: [1, 2, 5],
    4: [2, 5],
    5: [3, 4],
}
path = bfs_shortest_path(path_graph, start=0, end=5)
print(f"\nNajkrótsza ścieżka 0 → 5: {path}")

# Wykrywanie cykli
graph_with_cycle = {0: [1], 1: [2], 2: [0]}
graph_no_cycle = {0: [1], 1: [2], 2: []}
print(f"\nCykl w grafie 1: {has_cycle(graph_with_cycle)}")   # True
print(f"Cykl w grafie 2: {has_cycle(graph_no_cycle)}")        # False

# Sortowanie topologiczne
dag = {0: [], 1: [], 2: [3], 3: [1], 4: [0, 1], 5: [0, 2]}
order = topological_sort(dag)
print(f"\nKolejność topologiczna: {order}")
