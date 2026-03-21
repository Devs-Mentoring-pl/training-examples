# Szkolenie 2: GraphQL -- Strawberry i Django w praktyce

Kompletne GraphQL API z Django i Strawberry: typy, query, mutations (CRUD),
filtry, paginacja, autentykacja, permissions.

## Pliki

- `models.py` -- model Article
- `types.py` -- ArticleType, UserType, ArticleInput, ArticlePartialInput, ArticleFilter
- `schema.py` -- Query + Mutation + schema
- `permissions.py` -- IsAuthenticated, IsStaff, IsAuthor
- `urls.py` -- endpoint /graphql/

## Wymagania

```bash
pip install django strawberry-graphql-django
```

## Konfiguracja settings.py

```python
INSTALLED_APPS = [
    # ...
    "strawberry_django",
]
```
