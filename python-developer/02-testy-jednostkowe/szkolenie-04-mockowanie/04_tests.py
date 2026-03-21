# tests.py – mockowanie stałych

import application
from application import double


def test_mocking_constant_a(mocker):
    mocker.patch.object(application, 'CONSTANT_A', 2)
    expected = 4
    actual = double()

    assert expected == actual
