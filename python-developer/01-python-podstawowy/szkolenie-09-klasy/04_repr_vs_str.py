"""
Szkolenie 9 Klasy - Przyklad 4
__repr__ vs __str__ - reprezentacja obiektu dla developera i uzytkownika.
"""


class Vehicle:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year

    def __str__(self):
        return f"{self.brand} ({self.year})"

    def __repr__(self):
        return f"Vehicle(brand={self.brand!r}, year={self.year!r})"


def main():
    car = Vehicle("Audi", 2023)

    print(str(car))    # __str__ - dla uzytkownika
    print(repr(car))   # __repr__ - dla developera

    # W liscie Python uzywa __repr__:
    cars = [Vehicle("Audi", 2023), Vehicle("BMW", 2021)]
    print(cars)


if __name__ == "__main__":
    main()
