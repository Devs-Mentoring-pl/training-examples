"""
Szkolenie 2 Dekoratory - Przyklad 4
Uniwersalny dekorator z *args i **kwargs.
"""


def make_universal(func):
    def inner(*args, **kwargs):
        print("Got decorated")
        return func(*args, **kwargs)

    return inner

@make_universal
def ordinary_no_params():
    print("No params")

@make_universal
def ordinary_two_params(param1, param2):
    print(f"Two params: {param1}, {param2}")

ordinary_no_params()
ordinary_two_params("One", "Two")
