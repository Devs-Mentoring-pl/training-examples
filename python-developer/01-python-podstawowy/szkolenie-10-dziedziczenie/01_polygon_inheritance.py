"""
Szkolenie 10 Dziedziczenie - Przyklad 1
Dziedziczenie - klasa Polygon i Triangle z wzorem Herona.
"""


class Polygon:
    def __init__(self, sides_, angle_sum_):
        self.sides = sides_
        self.angle_sum = angle_sum_

    def calculate_perimeter(self):
        return sum(self.sides)

    def display_angle_sum(self):
        print(self.angle_sum)


class Triangle(Polygon):
    def __init__(self, a, b, c):
        super().__init__([a, b, c], 180)

    # Pole liczone z wzoru Herona
    def calculate_area(self):
        a, b, c = self.sides[0], self.sides[1], self.sides[2]
        p = (self.sides[0] + self.sides[1] + self.sides[2]) / 2
        return (p * (p - a) * (p - b) * (p - c)) ** 0.5


def main():
    equilateral_triangle = Triangle(5, 5, 5)
    print(equilateral_triangle.calculate_perimeter())
    equilateral_triangle.display_angle_sum()
    print(f"{equilateral_triangle.calculate_area():.4f}")


if __name__ == "__main__":
    main()
