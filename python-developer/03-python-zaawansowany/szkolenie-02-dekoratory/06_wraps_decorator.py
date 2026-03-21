"""
Szkolenie 2 Dekoratory - Przyklad 6
Uzycie @wraps z functools do zachowania metadanych dekorowanej funkcji.
"""

from functools import wraps


def add_stars(func):
    @wraps(func)
    def inner(*args, **kwargs):
        print(kwargs['amount'] * '*')
        func(*args, **kwargs)
        print(kwargs['amount'] * '*')

    return inner

@add_stars
def print_menu(*args, **kwargs):
    print(args[0])

print(f"Function name: {print_menu.__name__}")
print_menu("1. Start\n2. Exit", amount=17)
