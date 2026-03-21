# tests/test_even_mul.py
import pytest
from functionality.mul_only_even import *


def test_expect_exception_when_odd_num():
    with pytest.raises(NoEvenNumberHereException):
        mul_only_even(3, 1)


def test_expect_no_exception_when_even_nums():
    result = mul_only_even(2, 4)
    assert result == 8
