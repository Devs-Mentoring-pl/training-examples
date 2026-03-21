"""
Szkolenie 2 Dekoratory - Przyklad 5
Dekorator rysujacy ramke z gwiazdek wokol tekstu menu.
"""


def add_stars(func):
    def inner(*args, **kwargs):
        print(kwargs['amount'] * '*')
        func(*args, **kwargs)
        print(kwargs['amount'] * '*')

    return inner

@add_stars
def print_menu(*args, **kwargs):
    print(args[0])

print_menu("1. Start\n2. Exit", amount=17)
