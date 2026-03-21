"""
Szkolenie 10 Dziedziczenie - Przyklad 2
Gra RPG - dziedziczenie z rozszerzeniem metod (super().tell()).
"""


class Character:
    def __init__(self, name, start_items, abilities_):
        self.player_name = name
        self.hp = 100
        self.gold = 50
        self.inventory = start_items  # list for ala-items in inv
        self.abilities = abilities_   # dictionary for abilities specific for a character

    def add_to_inventory(self, new_item):
        self.inventory.append(new_item)

    def use_ability(self, name):
        if name in self.abilities:
            print(self.abilities.get(name))
        else:
            print("Unknown ability!")

    def tell(self):
        print("Howdy, I'm", self.player_name)


class Blacksmith(Character):
    def __init__(self, name):
        super().__init__(name, ['hammer'], {'improving items': 'an item has been improved...'})

    def tell(self):
        super().tell()
        print("I can repair your stuff...")


class Elf(Character):
    def __init__(self, name):
        super().__init__(name, ['bow', 'knife'], {'shooting': 'just shot a bow...', 'attack':
                         'just attacked enemy with knife...'})

    def tell(self):
        super().tell()
        print("Fight or die...")


if __name__ == "__main__":
    elf = Elf("Legolas")
    blacksmith = Blacksmith("Jack")

    elf.tell()
    elf.add_to_inventory('item1')
    elf.use_ability('shooting')

    print()  # space as an empty line

    blacksmith.tell()
    blacksmith.use_ability('attack')
