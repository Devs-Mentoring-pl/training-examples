"""
Facade - inteligentny dom.

Fasada (RemoteControl) zapewnia uproszczony interfejs,
który deleguje realizację złożonych funkcjonalności
do odpowiednich komponentów systemu (światło, drzwi).
"""


class HallLight:
    def __init__(self):
        self.name = "Hall Light 2.0"
        print("Hall Light's been added to the system!")

    def light(self):
        print(f"{self.name}'s been lighted!")

    def switch_off(self):
        print(f"{self.name}'s been switched off!")


class MainDoor:
    def __init__(self):
        self.name = "Wooden Main Door"
        print("Wooden Main Door's been added to the system!")

    def open(self):
        print(f"{self.name}'s been opened!")

    def close(self):
        print(f"{self.name}'s been closed!")


class GarageDoor:
    def __init__(self):
        self.name = "Solid Garage Door"
        print("Garage Door's been added to the system")

    def open(self):
        print(f"{self.name}'s been opened!")

    def close(self):
        print(f"{self.name}'s been closed!")


class RemoteControl:
    """Fasada - jeden pilot do sterowania całym domem"""

    def __init__(self):
        self.hall_light = HallLight()
        self.doors = {"main_door": MainDoor(), "garage_door": GarageDoor()}

    def close_doors(self):
        print("Closing all doors!")
        for door in self.doors:
            self.doors[door].close()
        print()

    def open_doors(self):
        print("Opening all doors!")
        for door in self.doors:
            self.doors[door].open()
        print()

    def light_hall(self):
        self.hall_light.light()
        print()

    def switch_off_hall(self):
        self.hall_light.switch_off()
        print()


# Kod kliencki - proste polecenia, zero wiedzy o komponentach
if __name__ == "__main__":
    remote = RemoteControl()
    remote.open_doors()
    remote.light_hall()
    remote.switch_off_hall()
    remote.close_doors()
