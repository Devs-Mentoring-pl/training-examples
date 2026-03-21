"""
Szkolenie 9 Klasy - Przyklad 5
Kopie plytkie i glebokie - problem z referencjami do obiektow.
"""

import copy


class Item:
    def __init__(self, name):
        self.name = name


class Box:
    def __init__(self, item_name):
        self.item = Item(item_name)  # pole jest obiektem innej klasy!
        self.num_elements = 1


def main():
    equipment_box = Box("laptop")

    # Kopia plytka - zagniezdzone obiekty NIE sa kopiowane:
    shallow_copy = copy.copy(equipment_box)
    shallow_copy.item.name = "Telewizor"
    shallow_copy.num_elements = 2

    print("Kopia plytka:")
    print(f"  Oryginal item: {equipment_box.item.name}")  # "Telewizor" - zmienione!
    print(f"  Oryginal num_elements: {equipment_box.num_elements}")  # 1 - OK

    # Kopia gleboka - kopiuje WSZYSTKO:
    equipment_box2 = Box("laptop")
    deep_copy = copy.deepcopy(equipment_box2)
    deep_copy.item.name = "Monitor"
    deep_copy.num_elements = 3

    print("\nKopia gleboka:")
    print(f"  Oryginal item: {equipment_box2.item.name}")  # "laptop" - niezmienione!
    print(f"  Oryginal num_elements: {equipment_box2.num_elements}")  # 1 - OK


if __name__ == "__main__":
    main()
