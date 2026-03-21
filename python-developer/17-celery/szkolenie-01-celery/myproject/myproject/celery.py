import os

from celery import Celery

# Ustawiamy domyślny moduł ustawień Django dla programu 'celery'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

app = Celery("myproject")

# Ładujemy konfigurację Celery z ustawień Django
# Prefiks CELERY_ oznacza, że wszystkie ustawienia Celery
# w settings.py muszą zaczynać się od CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatycznie znajduje taski w zainstalowanych aplikacjach Django
# Szuka plików tasks.py w każdej aplikacji z INSTALLED_APPS
app.autodiscover_tasks()
