# tests.py – mockowanie metody w klasie

from application import get_data


def test_mocking_class_method(mocker):
    expected = 'some data'

    def mock_load_data(self):
        val = 'some'
        return val + ' data'  # pokazujemy, że można zamockować całą metodę

    mocker.patch('application.Data.load_data', mock_load_data)

    actual = get_data()

    assert expected == actual
