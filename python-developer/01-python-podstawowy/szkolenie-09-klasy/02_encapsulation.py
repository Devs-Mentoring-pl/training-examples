"""
Szkolenie 9 Klasy - Przyklad 2
Enkapsulacja - pola prywatne, chronione, publiczne + gettery/settery.
"""


class Vehicle:
    def __init__(self, num_wheels, brand, paint_color):
        self.__num_wheels = num_wheels        # pole prywatne
        self._brand = brand                    # pole chronione (protected)
        self.paint_color = paint_color         # pole publiczne

    ''' getter pola __num_wheels '''
    def get_num_wheels(self):
        return self.__num_wheels

    ''' setter pola __num_wheels '''
    def set_num_wheels(self, num_wheels):
        self.__num_wheels = num_wheels


def main():
    passenger_car = Vehicle(4, "Audi", "niebieski")
    heavy_truck = Vehicle(10, "Ashok Leyland", "żółty")

    # Uzyj gettera:
    print(passenger_car.get_num_wheels())

    # Pole chronione - dostepne, ale konwencja mowi "nie dotykaj":
    print(passenger_car._brand)

    # Pole publiczne - bez ograniczen:
    print(passenger_car.paint_color)

    # Uzyj settera:
    heavy_truck.set_num_wheels(12)
    print(heavy_truck.get_num_wheels())


if __name__ == "__main__":
    main()
