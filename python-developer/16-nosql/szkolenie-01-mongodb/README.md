# Szkolenie 1: NoSQL i MongoDB

Przyklady pracy z MongoDB z poziomu Pythona: pymongo 4.x (synchroniczny driver)
oraz Motor (asynchroniczny driver). CRUD, aggregation pipeline, obsluga bledow.

## Pliki

- `01_crud.py` -- podstawowe operacje CRUD z pymongo
- `02_aggregation.py` -- przyklad aggregation pipeline
- `03_async_motor.py` -- asynchroniczny driver Motor

## Wymagania

```bash
pip install pymongo motor
```

## MongoDB

Uruchom MongoDB lokalnie lub w Dockerze:

```bash
docker run -d --name mongodb -p 27017:27017 -v mongodb_data:/data/db mongo:8.0
```
