# Szkolenie 4: Rejestracja uzytkownikow

Kompletny system rejestracji uzytkownikow z rozszerzonym formularzem (pole email),
obsluga GET/POST, messages framework, crispy-forms z Bootstrap 5.

## Pliki

- `forms.py` -- UserRegisterForm rozszerzajacy UserCreationForm o pole email
- `views.py` -- widok rejestracji z obsluga POST i komunikatem sukcesu
- `urls.py` -- konfiguracja URL-i projektu (register, login, logout, blog)

## Wymagania

```bash
pip install django django-crispy-forms crispy-bootstrap5
```

## Konfiguracja settings.py

```python
INSTALLED_APPS = [
    # ...
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    'crispy_forms',
    'crispy_bootstrap5',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
```
