"""
Szkolenie 2 – Mangum handler dla Django (ASGI).

Mangum opakowuje aplikację ASGI Django i tłumaczy
event API Gateway na żądanie ASGI.

UWAGA: Ten plik wymaga zainstalowanego pakietu 'mangum'
oraz projektu Django z modułem 'myproject.asgi'.
Uruchom go w środowisku Lambda, nie lokalnie.
"""

try:
    from mangum import Mangum
    from myproject.asgi import application

    # Mangum opakowuje aplikację ASGI Django
    # i tłumaczy event API Gateway → żądanie ASGI
    handler = Mangum(application, lifespan="off")
except ImportError as e:
    print(f"Import pominięty (brak zależności: {e})")
    print("Ten plik jest przeznaczony do uruchomienia na AWS Lambda.")
    handler = None
