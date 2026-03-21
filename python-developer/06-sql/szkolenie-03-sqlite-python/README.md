# Szkolenie 3 - SQLite3 w Pythonie

Przykłady kodu z materiału szkoleniowego dotyczącego integracji SQLite3 z Pythonem.

## Pliki

| Plik | Opis |
|------|------|
| `01_connect_and_create.py` | Tworzenie bazy, kursora, tabeli `users` |
| `02_insert_and_select.py` | Placeholdery `?`, `executemany()`, `fetchall()`, `fetchone()` |
| `03_row_factory.py` | `row_factory = sqlite3.Row` - dostęp po nazwie kolumny |
| `04_database_class.py` | Klasa `Database` z context managerem (`__enter__`/`__exit__`) |
| `05_memory_database.py` | Baza w pamięci (`:memory:`), `contextlib.closing` |

## Uruchomienie

```bash
python 01_connect_and_create.py
```

Skrypty 01-03 tworzą plik `example_database.sqlite3` w bieżącym katalogu. Skrypt 04 tworzy i usuwa plik tymczasowy. Skrypt 05 działa wyłącznie w pamięci.

Wszystkie przykłady korzystają wyłącznie z biblioteki standardowej.
