# Szkolenie 6 - Wielowątkowość

Przykłady kodu z materiału szkoleniowego dotyczącego wielowątkowości w Pythonie.

## Pliki

| Plik | Opis |
|------|------|
| `01_basic_thread.py` | Utworzenie i uruchomienie pojedynczego wątku |
| `02_multithreaded_calc.py` | Dwa współbieżne wątki z `time.sleep()` |
| `03_data_race.py` | Problem data race - niedeterministyczny wynik |
| `04_lock_fix.py` | Rozwiązanie data race z `threading.Lock` |
| `05_deadlock.py` | Przykład deadlocka (program zawiesi się celowo!) |

## Uruchomienie

```bash
python 01_basic_thread.py
```

Wszystkie przykłady korzystają wyłącznie z biblioteki standardowej.
