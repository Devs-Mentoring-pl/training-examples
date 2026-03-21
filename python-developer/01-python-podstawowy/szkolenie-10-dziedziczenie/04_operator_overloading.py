"""
Szkolenie 10 Dziedziczenie - Przyklad 4
Przeladowanie operatorow - metoda specjalna __add__.
"""


class Area:
    def __init__(self, surface_):
        self.surface = surface_

    def __add__(self, obj):
        return self.surface + obj.surface


def main():
    area1 = Area(100)
    area2 = Area(200)

    print(area1 + area2)  # 300


if __name__ == "__main__":
    main()
