# Szkolenie 5: FastAPI - Zaawansowane tematy

Przykłady zaawansowanych funkcji FastAPI: Background Tasks, WebSockets, Middleware, testowanie i deployment z Dockerem.

## Pliki

| Plik | Opis |
|------|------|
| `01_background_tasks.py` | BackgroundTasks - wysyłanie e-maili i logowanie w tle |
| `02_websocket_chat.py` | WebSocket chat z ConnectionManager |
| `02_chat_client.html` | Klient HTML do testowania czatu WebSocket |
| `03_middleware.py` | Custom middleware - TimingMiddleware, LoggingMiddleware |
| `04_testing.py` | Testy z TestClient, async testy, dependency overrides |
| `Dockerfile` | Multi-stage build dla FastAPI |
| `docker-compose.yaml` | FastAPI + PostgreSQL |

## Jak uruchomić

```bash
pip install -r requirements.txt

# Background Tasks
fastapi dev 01_background_tasks.py

# WebSocket Chat
fastapi dev 02_websocket_chat.py
# Otwórz 02_chat_client.html w przeglądarce

# Middleware
fastapi dev 03_middleware.py

# Testy
pytest 04_testing.py -v
```

## Docker

```bash
docker compose build
docker compose up -d
docker compose logs -f api
docker compose down
```
