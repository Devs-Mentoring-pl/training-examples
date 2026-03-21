# Celery - Zadania asynchroniczne

Przykład z Szkolenia 1: Celery - Zadania asynchroniczne.

## Struktura projektu

```
myproject/
├── myproject/
│   ├── __init__.py          # Import celery_app
│   ├── celery.py            # Konfiguracja Celery
│   ├── celery_settings.py   # Ustawienia do settings.py (Celery + Beat + Routing)
│   └── ...
├── orders/
│   ├── tasks.py             # Definicje taskow (send_order_confirmation, retry, webhook, itp.)
│   └── views.py             # Widoki Django (delay, apply_async, AsyncResult)
├── compose.yaml             # Docker Compose (Django + Worker + Beat + Redis + Flower)
├── Dockerfile
└── requirements.txt
```

## Instalacja

```bash
pip install celery redis
```

## Uruchomienie (Docker Compose)

```bash
cd myproject
docker compose up --build
```

Po uruchomieniu:
- http://localhost:8000 - Django
- http://localhost:5555 - Flower (monitoring Celery)
- localhost:6379 - Redis

## Uruchomienie (lokalne)

```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Django
python manage.py runserver

# Terminal 3: Celery Worker
celery -A myproject worker --loglevel=info

# Terminal 4: Celery Beat (opcjonalnie)
celery -A myproject beat --loglevel=info
```

## Przyklady taskow

- `send_order_confirmation` - prosty task z `@shared_task`
- `call_external_api` - reczny retry z `bind=True`
- `send_webhook` - automatyczny retry z `autoretry_for` i backoff
- `process_payment` - `acks_late=True` dla bezpieczenstwa
- `generate_report` - task z `time_limit` i `soft_time_limit`

## Komendy Celery CLI

```bash
celery -A myproject inspect active       # Aktywne taski
celery -A myproject inspect registered   # Zarejestrowane taski
celery -A myproject inspect ping         # Ping workerow
celery -A myproject inspect stats        # Statystyki
```
