"""
Szkolenie 2 – Mangum handler dla FastAPI.

UWAGA: Ten plik wymaga zainstalowanego pakietu 'mangum'
oraz modułu 'main' z aplikacją FastAPI.
Uruchom go w środowisku Lambda, nie lokalnie.
"""

try:
    from mangum import Mangum
    from main import app  # Twoja aplikacja FastAPI

    handler = Mangum(app)
except ImportError as e:
    print(f"Import pominięty (brak zależności: {e})")
    print("Ten plik jest przeznaczony do uruchomienia na AWS Lambda.")
    handler = None
