"""
Szkolenie 5 Exceptions - Przyklad 3
Pelny blok try/except/else/finally.
"""

import tempfile
import os


# Przyklad 1: Walidacja wieku
print("=== try/except/else: walidacja ===")

test_inputs = ["25", "abc", "17"]

for test_input in test_inputs:
    print(f"\nWejscie: '{test_input}'")
    try:
        age = int(test_input)
    except ValueError:
        print("  Nieprawidlowa wartosc!")
    else:
        if age <= 21:
            print("  Nie mozesz wejsc, za mlody.")
        else:
            print("  Witaj, jestes wystarczajaco dorosly.")


# Przyklad 2: Operacje na pliku z finally
print("\n=== try/except/else/finally: plik ===")

# Tworzenie tymczasowego pliku do testu
tmp_file = os.path.join(tempfile.gettempdir(), "test_exceptions.txt")

file = open(tmp_file, 'w')
try:
    file.write("Testing exception handling.")
    print("Zapisywanie do pliku...")
except OSError:
    print("Nie udalo sie zapisac do pliku!")
else:
    print("Zapis udany.")
finally:
    file.close()
    print("Plik zamkniety (finally).")

# Odczyt dla weryfikacji
with open(tmp_file, 'r') as f:
    print(f"Zawartosc pliku: {f.read()}")

# Sprzatanie
os.remove(tmp_file)


# Przyklad 3: Zasada minimalizacji kodu w try
print("\n=== Zasada: minimalizuj kod w try ===")

test_value = "42"

# Dobrze - w try tylko ryzykowna linia
try:
    value = int(test_value)
except ValueError:
    print("Podana wartosc musi byc liczba!")
else:
    print(f"Twoja podana liczba to: {value}")
    print(f"Podwojona: {value * 2}")
finally:
    print("Koniec operacji.")
