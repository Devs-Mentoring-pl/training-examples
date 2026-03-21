# tests/test_arith_seq.py
from functionality.operations import *


def test_should_return_correct_sum_for_positive_range():
    start = 1
    end = 10

    assert calc_arith_seq_sum(start, end) == 55

    start = 5
    end = 15

    assert calc_arith_seq_sum(start, end) == 110


def test_should_return_correct_sum_for_1_long_seq():
    start = 5
    end = start

    assert calc_arith_seq_sum(start, end) == start


def test_should_return_correct_sum_for_negative_range():
    start = -100
    end = -10

    assert calc_arith_seq_sum(start, end) == -5005


def test_should_return_correct_sum_for_various_range():
    start = -5
    end = 10

    assert calc_arith_seq_sum(start, end) == 40
