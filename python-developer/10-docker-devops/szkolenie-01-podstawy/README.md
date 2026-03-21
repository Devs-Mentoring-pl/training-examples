# Flask Docker - Podstawy

Prosta aplikacja Flask uruchomiona w kontenerze Docker.

## Struktura projektu

```
flask_docker/
├── src/
│   └── app.py
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

## Budowanie obrazu

```bash
docker build -t flask_app .
```

## Uruchomienie kontenera

```bash
docker run -d -p 5000:5000 --name flask_container flask_app
```

Aplikacja dostępna pod: http://localhost:5000

## Endpointy

- `GET /` - komunikat powitalny
- `GET /health` - health check (`{"status": "ok"}`)

## Zatrzymanie i usunięcie

```bash
docker rm -f flask_container
```
