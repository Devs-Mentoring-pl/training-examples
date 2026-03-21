# tests.py – Z mockami (testy wykonują się błyskawicznie)

import pytest
from application import do_calculation


@pytest.fixture
def set_api_mock(mocker):
    mocker.patch('application.call_api', return_value=100)


def test_compute_for_positive_value(set_api_mock):
    expected = 105
    actual = 5
    assert do_calculation(actual) == expected


def test_compute_for_negative_value(set_api_mock):
    expected = 90
    actual = -10
    assert do_calculation(actual) == expected


def test_compute_for_zero(set_api_mock):
    expected = 100
    actual = 0
    assert do_calculation(actual) == expected
