# Django + PostgreSQL + Redis - Docker Compose

Środowisko developerskie dla aplikacji Django z bazą danych PostgreSQL i cache Redis.

## Struktura projektu

```
django-postgres-redis/
├── compose.yaml
├── Dockerfile
├── requirements.txt
├── .env.example
└── myapp/
    ├── manage.py
    └── myapp/
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```

## Uruchomienie

1. Skopiuj plik `.env.example` do `.env`:

```bash
cp .env.example .env
```

2. Uruchom wszystkie serwisy:

```bash
docker compose up -d --build
```

3. Uruchom migracje Django:

```bash
docker compose exec web python myapp/manage.py migrate
```

4. Utwórz superusera:

```bash
docker compose exec web python myapp/manage.py createsuperuser
```

Aplikacja dostępna pod: http://localhost:8000

## Zatrzymanie

```bash
docker compose down
```

## Zatrzymanie z usunięciem danych (volumes)

```bash
docker compose down -v
```
