# tests/markers.py
import pytest


@pytest.mark.greater
def test_greater():
    num = 1000
    assert num > 100


@pytest.mark.equal
def test_equal():
    num = 5
    assert num == 10


@pytest.mark.others
def test_str_comparison():
    examp = "examp1"
    assert examp == "examp1"


@pytest.mark.others
def test_reversed_str_comparison():
    examp = "examp1"
    examp = examp[::-1]

    assert examp == "1pmaxe"
