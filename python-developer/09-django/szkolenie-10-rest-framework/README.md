# Szkolenie 10: Django REST Framework

Kompletne REST API z Django REST Framework -- od serializera przez widoki
funkcyjne (@api_view), klasowe (APIView), generic views, az po ViewSet + Router.
Obejmuje customizacje serializera, uprawnienia i JWT.

## Pliki

- `models.py` -- model Article
- `serializers.py` -- ArticleSerializer z nested UserSerializer, walidacja, SerializerMethodField
- `views.py` -- ViewSet z perform_create i permission_classes
- `urls.py` -- Router z automatycznymi URL-ami + endpointy JWT
- `permissions.py` -- custom IsAuthorOrReadOnly permission

## Wymagania

```bash
pip install django djangorestframework djangorestframework-simplejwt django-filter
```

## Konfiguracja settings.py

```python
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    # ...
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```
