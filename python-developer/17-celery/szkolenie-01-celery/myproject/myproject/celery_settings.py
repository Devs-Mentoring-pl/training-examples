"""
Ustawienia Celery do dodania w settings.py projektu Django.
"""

import os

from celery.schedules import crontab

# === Celery ===
CELERY_BROKER_URL = os.environ.get(
    "CELERY_BROKER_URL", "redis://localhost:6379/0"
)
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379/0"
)

# Serializacja – JSON jest bezpieczniejszy niż pickle
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# Strefa czasowa – zgodna z TIME_ZONE Django
CELERY_TIMEZONE = "Europe/Warsaw"

# Śledzenie statusu tasku (PENDING → STARTED → SUCCESS/FAILURE)
CELERY_TASK_TRACK_STARTED = True

# Jak długo przechowywać wyniki (w sekundach) – domyślnie 24h
CELERY_RESULT_EXPIRES = 3600 * 24

# === Periodic Tasks (Celery Beat) ===
CELERY_BEAT_SCHEDULE = {
    # Co 10 minut – czyść wygasłe sesje
    "cleanup-expired-sessions": {
        "task": "accounts.tasks.cleanup_expired_sessions",
        "schedule": 600.0,  # co 600 sekund = 10 minut
    },

    # Codziennie o 8:00 – wyślij raport dzienny
    "daily-sales-report": {
        "task": "reports.tasks.send_daily_report",
        "schedule": crontab(hour=8, minute=0),
    },

    # Co poniedziałek o 9:00 – newsletter
    "weekly-newsletter": {
        "task": "newsletters.tasks.send_weekly_newsletter",
        "schedule": crontab(hour=9, minute=0, day_of_week="monday"),
    },

    # Pierwszy dzień miesiąca o północy
    "monthly-invoice": {
        "task": "billing.tasks.generate_monthly_invoices",
        "schedule": crontab(day_of_month=1, hour=0, minute=0),
    },

    # Task z argumentami
    "check-stock-levels": {
        "task": "warehouse.tasks.check_stock",
        "schedule": crontab(hour="*/2"),  # co 2 godziny
        "args": (10,),  # próg minimalny = 10 sztuk
    },
}

# === Task Routing ===
CELERY_TASK_ROUTES = {
    "orders.tasks.send_email": {"queue": "emails"},
    "reports.tasks.*": {"queue": "reports"},
    "imports.tasks.*": {"queue": "imports"},
}

CELERY_TASK_DEFAULT_QUEUE = "default"
