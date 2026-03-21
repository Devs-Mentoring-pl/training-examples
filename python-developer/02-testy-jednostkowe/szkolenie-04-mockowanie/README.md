# PyTest - Mockowanie

Przykłady z Szkolenia 4: PyTest - Mockowanie.

## Instalacja

```bash
pip install -r requirements.txt
```

## Przykłady

Każdy przykład składa się z pliku application (kod produkcyjny) i pliku tests (testy):

### 01 - Mockowanie funkcji
- `01_application.py` - `do_calculation()` i `call_api()` z `time.sleep(10)`
- `01_tests_no_mock.py` - testy BEZ mockow (~30 sekund)
- `01_tests_with_mock.py` - testy Z mockami i fikstura (~0.06 sekundy)

### 02 - Mockowanie metody w klasie
- `02_application.py` - klasa `Data` z metoda `load_data()`
- `02_tests.py` - mock calej metody z wlasna funkcja zastepczą

### 03 - Mockowanie calej klasy
- `03_application.py` - klasa `MyClass` z kosztownym `__init__`
- `03_tests.py` - mock calej klasy i jej metod

### 04 - Mockowanie stalych
- `04_constants.py` - `CONSTANT_A = 10`
- `04_application.py` - `double()` korzystajaca z `CONSTANT_A`
- `04_tests.py` - mock stalej za pomoca `mocker.patch.object()`

## Uruchomienie

```bash
# Testy z mockami (szybkie)
pytest 01_tests_with_mock.py -v

# Testy bez mockow (wolne ~30s)
pytest 01_tests_no_mock.py -v
```

## Kluczowe koncepty

- `mocker.patch('modul.funkcja', return_value=wartosc)` - mockowanie funkcji
- `mocker.patch('modul.Klasa.metoda', mock_fn)` - mockowanie metody z wlasna funkcja
- `mocker.patch('modul.Klasa')` - mockowanie calej klasy
- `mocker.patch.object(modul, 'STALA', wartosc)` - mockowanie stalych
