# PyTest - Podstawy

Przykłady z Szkolenia 3: PyTest.

## Instalacja

```bash
pip install -r requirements.txt
```

## Struktura

```
functionality/
├── operations.py       # calc_power, calc_arith_seq_sum
└── mul_only_even.py    # mul_only_even + NoEvenNumberHereException

tests/
├── 01_test_power.py         # Testy potegowania (cykl TDD)
├── 02_test_arith_seq.py     # Testy sumy ciagu arytmetycznego
├── 03_markers.py            # Markery (@pytest.mark.greater, .equal, .others)
├── 04_fixture_examp.py      # Fikstury (@pytest.fixture)
├── 05_parametrize_examp.py  # Testy sparametryzowane (@pytest.mark.parametrize)
├── 06_advanced_parametrize.py # Sparametryzowane fikstury (indirect)
└── 07_test_even_mul.py      # Testowanie wyjatkow (pytest.raises)
```

## Uruchomienie

```bash
# Wszystkie testy
pytest tests/ -v

# Konkretny plik
pytest tests/01_test_power.py -v

# Konkretny marker
pytest -m others tests/03_markers.py -v

# Z pokryciem kodu
pytest --cov=tests/
```
