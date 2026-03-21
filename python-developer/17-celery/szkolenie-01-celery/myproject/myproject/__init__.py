# Importujemy aplikację Celery, żeby była dostępna
# od razu po starcie Django
from .celery import app as celery_app

__all__ = ("celery_app",)
