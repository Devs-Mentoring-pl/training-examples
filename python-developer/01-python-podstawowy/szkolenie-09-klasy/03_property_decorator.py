"""
Szkolenie 9 Klasy - Przyklad 3
Dekorator @property - pythonowy getter i setter z walidacja.
"""


class Person:
    def __init__(self, name, age):
        self.name = name
        self._age = age    # pole "chronione"

    @property
    def age(self):
        """Getter - zwraca wiek."""
        return self._age

    @age.setter
    def age(self, new_age):
        """Setter - waliduje przed ustawieniem."""
        if new_age < 0:
            raise ValueError("Wiek nie może być ujemny!")
        self._age = new_age


def main():
    person = Person("Kacper", 28)
    print(person.age)       # 28 - wywoluje getter

    person.age = 30          # wywoluje setter
    print(person.age)       # 30

    # Proba ustawienia ujemnego wieku:
    try:
        person.age = -5
    except ValueError as e:
        print(f"Blad: {e}")


if __name__ == "__main__":
    main()
