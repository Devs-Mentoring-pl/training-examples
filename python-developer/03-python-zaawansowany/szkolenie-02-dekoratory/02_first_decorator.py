"""
Szkolenie 2 Dekoratory - Przyklad 2
Tworzenie pierwszego dekoratora - skladnia @nazwa_dekoratora.
"""


def make_decorated(func):
    def inner():
        print("Got decorated")
        func()

    return inner


@make_decorated
def ordinary():
    print("I am ordinary")


ordinary()  # "Got decorated"
            # "I am ordinary"
