# tests.py – BEZ mocków (każdy test czeka 10 sekund na API)

from application import do_calculation


def test_compute_for_positive_value():
    expected = 105
    actual = 5
    assert do_calculation(actual) == expected


def test_compute_for_negative_value():
    expected = 90
    actual = -10
    assert do_calculation(actual) == expected


def test_compute_for_zero():
    expected = 100
    actual = 0
    assert do_calculation(actual) == expected
