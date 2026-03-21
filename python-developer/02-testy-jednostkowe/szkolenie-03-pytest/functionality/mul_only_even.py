class NoEvenNumberHereException(Exception):
    pass


def mul_only_even(a, b):
    if a % 2 or b % 2:
        raise NoEvenNumberHereException

    return a * b
