"""
Algorytmika - Szkolenie 5
Lista wiazana jednokierunkowa - pelna implementacja z testami.
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

    def __len__(self) -> int:
        curr = self.head
        counter = 0
        while curr:
            counter += 1
            curr = curr.next
        return counter

    def __str__(self) -> str:
        output = ''
        curr = self.head
        while curr:
            if curr == self.tail:
                output += str(curr.value)
            else:
                output += str(curr.value) + ' -> '
            curr = curr.next
        return output

    def find_by_idx(self, idx: int) -> Optional[Node]:
        counter = 0
        curr = self.head
        while counter != idx and curr is not None:
            curr = curr.next
            counter += 1
        return curr

    def remove_last(self) -> Any:
        if self.head is self.tail:
            removed_value = self.head.value
            self.head, self.tail = None, None
            return removed_value
        removed_node = self.tail
        new_tail = self.find_by_idx(idx=len(self) - 2)
        new_tail.next = None
        self.tail = new_tail
        return removed_node.value

    def remove(self, after_idx: int) -> Any:
        after = self.find_by_idx(after_idx)
        if after is self.tail:
            return None
        if after.next is self.tail:
            return self.remove_last()
        removed_node = after.next
        after.next = after.next.next
        return removed_node.value

    def pop(self) -> Any:
        if len(self) == 0:
            return None
        erased_node = self.head
        if self.head is self.tail:
            self.tail = self.tail.next
        self.head = self.head.next
        return erased_node.value


# --- Testy ---
list_ = LinkedList()

# Lista pusta
assert list_.head is None

# push - dodawanie na poczatek
list_.push(1)
list_.push(0)
assert str(list_) == '0 -> 1'

# push_back - dodawanie na koniec
list_.push_back(9)
list_.push_back(10)
assert str(list_) == '0 -> 1 -> 9 -> 10'

# find_by_idx + remove_last
last_element = list_.find_by_idx(idx=3)
returned_last_element = list_.remove_last()
assert last_element.value == returned_last_element
assert str(list_) == '0 -> 1 -> 9'

# remove - usuwanie elementu za podanym indeksem
list_.remove(1)
assert str(list_) == '0 -> 1'

print("Wszystkie testy przeszly!")
print(f"Lista: {list_}")
