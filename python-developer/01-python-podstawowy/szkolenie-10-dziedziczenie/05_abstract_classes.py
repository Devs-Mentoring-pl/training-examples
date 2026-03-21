"""
Szkolenie 10 Dziedziczenie - Przyklad 5
Klasy abstrakcyjne - ABC i @abstractmethod.
"""

from abc import ABC, abstractmethod
import math


class Shape(ABC):
    @abstractmethod
    def calculate_area(self):
        """Każda figura MUSI zaimplementować tę metodę."""
        pass

    @abstractmethod
    def calculate_perimeter(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def calculate_area(self):
        return math.pi * self.radius ** 2

    def calculate_perimeter(self):
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def calculate_area(self):
        return self.width * self.height

    def calculate_perimeter(self):
        return 2 * (self.width + self.height)


def main():
    circle = Circle(5)
    rectangle = Rectangle(4, 6)

    print(f"Koło: pole = {circle.calculate_area():.2f}, obwód = {circle.calculate_perimeter():.2f}")
    print(f"Prostokąt: pole = {rectangle.calculate_area()}, obwód = {rectangle.calculate_perimeter()}")

    # Proba utworzenia instancji klasy abstrakcyjnej:
    try:
        shape = Shape()
    except TypeError as e:
        print(f"\nNie mozna utworzyc instancji klasy abstrakcyjnej: {e}")


if __name__ == "__main__":
    main()
