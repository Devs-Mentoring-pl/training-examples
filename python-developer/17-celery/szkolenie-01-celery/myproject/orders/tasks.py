import time

import requests
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


# --- Prosty task ---

@shared_task
def send_order_confirmation(order_id: int) -> str:
    """Wysyła email z potwierdzeniem zamówienia."""
    # Symulacja wysyłania emaila (np. przez SMTP)
    time.sleep(5)

    # W prawdziwej aplikacji tutaj byłby kod wysyłający email
    # np. send_mail() z Django
    return f"Email wysłany dla zamówienia #{order_id}"


# --- Task z jawną nazwą ---

@shared_task(name="orders.send_confirmation")
def send_order_confirmation_named(order_id: int) -> str:
    """Wysyła email z potwierdzeniem zamówienia (jawna nazwa)."""
    time.sleep(5)
    return f"Email wysłany dla zamówienia #{order_id}"


# --- Ręczny retry ---

@shared_task(bind=True, max_retries=3)
def call_external_api(self, url: str) -> dict:
    """Wywołuje zewnętrzne API z obsługą retry."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        # Ponów za 60 sekund
        raise self.retry(exc=exc, countdown=60)


# --- Automatyczny retry (zalecany) ---

@shared_task(
    autoretry_for=(requests.RequestException, ConnectionError),
    max_retries=5,
    retry_backoff=True,       # wykładnicze opóźnienie: 1s, 2s, 4s, 8s, 16s
    retry_backoff_max=600,    # maksymalnie 10 minut między próbami
    retry_jitter=True,        # losowe odchylenie – zapobiega "thundering herd"
)
def send_webhook(url: str, payload: dict) -> int:
    """Wysyła webhook do partnera."""
    response = requests.post(url, json=payload, timeout=15)
    response.raise_for_status()
    return response.status_code


# --- acks_late – bezpieczeństwo przy awarii workera ---

@shared_task(
    acks_late=True,           # potwierdź dopiero PO wykonaniu
    reject_on_worker_lost=True,  # przy padnięciu workera – wrzuć z powrotem do kolejki
)
def process_payment(payment_id: int) -> str:
    """Przetwarza płatność – nie może być stracona."""
    # payment = Payment.objects.get(id=payment_id)
    # ... logika przetwarzania
    return f"Płatność #{payment_id} przetworzona"


# --- Task z timeoutem ---

@shared_task(
    time_limit=300,       # twardy limit – 5 minut, SIGKILL
    soft_time_limit=240,  # miękki limit – 4 minuty, rzuca SoftTimeLimitExceeded
)
def generate_report(report_id: int) -> str:
    try:
        # ... długa operacja
        return "Raport gotowy"
    except SoftTimeLimitExceeded:
        # Masz ~60 sekund na sprzątanie
        # Report.objects.filter(id=report_id).update(status="timeout")
        return "Raport przerwany – timeout"


# --- Task z logowaniem ---

@shared_task
def process_payment_logged(payment_id: int) -> str:
    logger.info("Rozpoczynam przetwarzanie płatności #%d", payment_id)
    # ... logika
    logger.info("Płatność #%d przetworzona pomyślnie", payment_id)
    return "OK"
