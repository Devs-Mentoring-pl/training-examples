# settings.py -- konfiguracja narzedzi do debugowania

# Django Debug Toolbar
INSTALLED_APPS = [
    # ...
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # ... reszta middleware
]

INTERNAL_IPS = [
    "127.0.0.1",
]

# django-extensions (shell_plus)
INSTALLED_APPS = [
    # ...
    "django_extensions",
]

# django-silk (alternatywny profiler, dziala z API/DRF)
INSTALLED_APPS = [
    # ...
    "silk",
]

MIDDLEWARE = [
    "silk.middleware.SilkyMiddleware",
    # ... reszta middleware
]
