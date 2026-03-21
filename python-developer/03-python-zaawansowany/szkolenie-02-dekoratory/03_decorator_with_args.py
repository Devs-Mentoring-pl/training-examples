"""
Szkolenie 2 Dekoratory - Przyklad 3
Dekorator z argumentami - walidacja dlugosci tekstu.
"""


def validate_less_than_10(func):
    def inner(txt: str):
        if len(txt) > 10:
            txt = 10 * '*'
        else:
            print("Valid txt!")

        func(txt)

    return inner


@validate_less_than_10
def say_hello(txt):
    print(f"Hello, {txt}")

say_hello("Kacper")
say_hello("Przybyslawa")
