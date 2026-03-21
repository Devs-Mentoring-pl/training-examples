"""
Szkolenie 2 Dekoratory - Przyklad 1
@classmethod jako metoda fabrykujaca (factory method).
"""

from datetime import date


class Worker:
    def __init__(self, name: str, start_year: int):
        self.name = name
        self.start_year = start_year

    @classmethod
    def fromSeniority(cls, name: str, years: int):
        return cls(name, date.today().year - years)

    def display(self):
        print(f"Worker's name: {self.name}\nWorker's start_year: {self.start_year}\n")


w1 = Worker("John", 2000)
w2 = Worker.fromSeniority("Elizabeth", 5)

w1.display()
w2.display()
