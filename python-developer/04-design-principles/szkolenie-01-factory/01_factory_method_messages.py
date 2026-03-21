"""
Factory Method - system komunikatów o błędach.

Wzorzec Factory Method wykorzystywany jest w momencie, gdy chcemy stworzyć
metodę (lub funkcję), która dostarczać nam będzie obiekty konkretnych klas.
Jaka to będzie klasa - zależy od wartości argumentu przesłanego do metody fabrykującej.
"""

import random
from abc import ABC


class Message(ABC):
    counter = 0

    def __init__(self):
        self.id = Message.counter
        Message.counter += 1

    def show(self):
        raise NotImplementedError


class HardwareMessage(Message):
    def __init__(self):
        super().__init__()
        self.show()

    def show(self):
        print(f"Problem with some internal component!, id: {self.id}")


class SoftwareMessage(Message):
    def __init__(self):
        super().__init__()
        self.show()

    def show(self):
        print(f"Problem with OS!, id: {self.id}")


def error_factory(is_error: bool = True):
    error_types = {b"0xf": HardwareMessage, b"0x0": SoftwareMessage}

    if is_error:
        rand_error = random.choice(list(error_types.keys()))
        error_types.get(rand_error)()


def main():
    for i in range(5):
        error_factory()


if __name__ == "__main__":
    main()
