"""
Szkolenie 10 Dziedziczenie - Przyklad 3
Dziedziczenie wielokrotne i MRO (Method Resolution Order).
"""


class Parent1:
    def __init__(self):
        super().__init__()
        print("In Parent1 class...")


class Parent2:
    def __init__(self):
        print("In Parent2 class...")


class Derived(Parent1, Parent2):
    def __init__(self):
        super().__init__()
        print("In Derived class...")


def main():
    d = Derived()
    print()
    print("MRO:", Derived.mro())


if __name__ == "__main__":
    main()
