# tests.py – mockowanie całej klasy

def test_with_mock(mocker):
    mock_my_class = mocker.patch('application.MyClass')
    mock_my_class_get_sth = mocker.patch('application.MyClass.get_something')
    mock_my_class_get_sth.return_value = 'Hello'

    assert mock_my_class.get_something() == 'Hello'
