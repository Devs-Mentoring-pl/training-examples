"""
Algorytmika - Szkolenie 5
Stos (LIFO) i kolejka (FIFO) - implementacja na bazie listy wiazanej.
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Node:
    value: Any
    next: Optional['Node'] = None


@dataclass
class LinkedList:
    head: Optional[Node] = None
    tail: Optional[Node] = None

    def push(self, value: Any) -> None:
        new_head = Node(value)
        new_head.next = self.head
        if self.head is None and self.tail is None:
            self.tail = new_head
        self.head = new_head

    def push_back(self, value: Any) -> None:
        new_tail = Node(value)
        if len(self) > 0:
            self.tail.next = new_tail
        else:
            self.head = new_tail
        self.tail = new_tail

    def pop(self) -> Any:
        if len(self) == 0:
            return None
        erased_node = self.head
        if self.head is self.tail:
            self.tail = self.tail.next
        self.head = self.head.next
        return erased_node.value

    def __len__(self) -> int:
        curr = self.head
        counter = 0
        while curr:
            counter += 1
            curr = curr.next
        return counter


# --- Stos (LIFO) ---
@dataclass
class Stack:
    _storage: LinkedList = None

    def __post_init__(self):
        if self._storage is None:
            self._storage = LinkedList()

    def push(self, value: Any) -> None:
        """Umieszcza element na wierzchu stosu."""
        self._storage.push(value)

    def pop(self) -> Any:
        """Zdejmuje i zwraca element z wierzchu stosu."""
        return self._storage.pop()

    def peek(self) -> Any:
        """Podglada wierzcholek stosu bez usuwania."""
        if self._storage.head is None:
            return None
        return self._storage.head.value

    def __len__(self) -> int:
        return len(self._storage)

    def __str__(self) -> str:
        output = ''
        curr = self._storage.head
        while curr:
            output += str(curr.value) + '\n'
            curr = curr.next
        return output


# --- Kolejka (FIFO) ---
@dataclass
class Queue:
    _storage: LinkedList = None

    def __post_init__(self):
        if self._storage is None:
            self._storage = LinkedList()

    def enqueue(self, value: Any) -> None:
        """Dodaje element na koniec kolejki."""
        self._storage.push_back(value)

    def dequeue(self) -> Any:
        """Usuwa i zwraca element z poczatku kolejki."""
        return self._storage.pop()

    def peek(self) -> Any:
        """Podglada pierwszy element kolejki bez usuwania."""
        if self._storage.head is None:
            return None
        return self._storage.head.value

    def __str__(self) -> str:
        output = ''
        curr = self._storage.head
        while curr:
            if curr is self._storage.tail:
                output += str(curr.value)
            else:
                output += str(curr.value) + ', '
            curr = curr.next
        return output

    def __len__(self) -> int:
        return len(self._storage)


# --- Testy stosu ---
stack = Stack()
assert len(stack) == 0

stack.push(3)
stack.push(10)
stack.push(1)
assert len(stack) == 3

top_value = stack.pop()
assert top_value == 1
assert len(stack) == 2
assert stack.peek() == 10

print("Stos:")
print(stack)

# --- Testy kolejki ---
queue = Queue()
assert len(queue) == 0

queue.enqueue('klient1')
queue.enqueue('klient2')
queue.enqueue('klient3')
assert str(queue) == 'klient1, klient2, klient3'

client_first = queue.dequeue()
assert client_first == 'klient1'
assert str(queue) == 'klient2, klient3'
assert len(queue) == 2
assert queue.peek() == 'klient2'

print("Kolejka:", queue)
print("\nWszystkie testy przeszly!")
