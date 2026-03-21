# Szkolenie 3: Panel admina, modele i migracje

Przykład modelu `Article` z relacją `ForeignKey` do wbudowanego modelu `User`,
rejestracja w panelu admina z zaawansowaną konfiguracją oraz widok wyświetlający
dane z bazy.

## Pliki

- `models.py` -- model Article z polami CharField, TextField, DateTimeField, ForeignKey
- `admin.py` -- rejestracja modelu z list_display, list_filter, search_fields
- `views.py` -- widok strony głównej pobierający artykuły z bazy

## Uruchomienie

```bash
pip install django
django-admin startproject first_project .
python manage.py startapp blog
# Skopiuj pliki do blog/
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
