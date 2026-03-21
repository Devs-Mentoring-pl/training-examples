"""
Szkolenie 9 Klasy - Przyklad 1
Klasa Vehicle z konstruktorem, polami i metodami.
"""


class Vehicle:
    def __init__(self, num_wheels, brand, paint_color):
        self.num_wheels = num_wheels
        self.brand = brand
        self.paint_color = paint_color

    def describe_vehicle(self):
        print("Znajdujesz się w pojeździe, który: ")
        print(f"Ma {self.num_wheels} kół, jest marki {self.brand} i jest koloru {self.paint_color}")


def main():
    passenger_car = Vehicle(4, "Audi", "niebieski")
    heavy_truck = Vehicle(10, "Ashok Leyland", "żółty")

    passenger_car.describe_vehicle()
    heavy_truck.describe_vehicle()


if __name__ == "__main__":
    main()
