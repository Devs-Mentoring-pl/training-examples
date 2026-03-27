# saga/order_saga.py
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class SagaStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    FAILED = "failed"


@dataclass
class SagaState:
    """Stan sagi – przechowywany w bazie lub Redis."""
    saga_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    order_id: str = ""
    status: SagaStatus = SagaStatus.PENDING
    completed_steps: list[str] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


# --- KROK 1: Serwis zamówień ---

def start_order_saga(customer_id: str, items: list[dict]) -> str:
    """Inicjuje sagę dla zamówienia."""
    order_id = str(uuid.uuid4())
    saga = SagaState(order_id=order_id)

    save_saga_state(saga)

    publish_event("order.saga.started", {
        "saga_id": saga.saga_id,
        "order_id": order_id,
        "customer_id": customer_id,
        "items": items,
    })

    return order_id


# --- KROK 2: Serwis płatności ---

def handle_saga_started(event_data: dict) -> None:
    """Płatność reaguje na start sagi."""
    saga_id = event_data["saga_id"]
    order_id = event_data["order_id"]
    total = sum(item["price"] for item in event_data["items"])

    try:
        charge_customer(event_data["customer_id"], total)

        publish_event("payment.succeeded", {
            "saga_id": saga_id,
            "order_id": order_id,
            "amount": total,
        })

    except PaymentError as e:
        publish_event("payment.failed", {
            "saga_id": saga_id,
            "order_id": order_id,
            "reason": str(e),
        })


# --- KROK 3: Serwis magazynowy ---

def handle_payment_succeeded(event_data: dict) -> None:
    """Magazyn reaguje na sukces płatności."""
    saga_id = event_data["saga_id"]
    order_id = event_data["order_id"]

    try:
        reserve_stock(order_id)

        publish_event("stock.reserved", {
            "saga_id": saga_id,
            "order_id": order_id,
        })

    except OutOfStockError as e:
        publish_event("stock.reservation.failed", {
            "saga_id": saga_id,
            "order_id": order_id,
            "reason": str(e),
        })


# --- KOMPENSACJA: Cofnięcie płatności ---

def handle_stock_reservation_failed(event_data: dict) -> None:
    """Płatność kompensuje – zwraca pieniądze klientowi."""
    saga_id = event_data["saga_id"]
    order_id = event_data["order_id"]

    refund_customer(order_id)

    publish_event("payment.refunded", {
        "saga_id": saga_id,
        "order_id": order_id,
        "reason": "Brak towaru w magazynie",
    })

    saga = load_saga_state(saga_id)
    saga.status = SagaStatus.FAILED
    save_saga_state(saga)


# --- Helpers (uproszczone) ---

def publish_event(event_type: str, payload: dict) -> None:
    print(f"[EVENT] {event_type}: {json.dumps(payload, ensure_ascii=False)}")


def save_saga_state(saga: SagaState) -> None:
    print(f"[SAGA] Zapisuję stan: {saga.saga_id} -> {saga.status}")


def load_saga_state(saga_id: str) -> SagaState:
    return SagaState(saga_id=saga_id)  # uproszczenie


def charge_customer(customer_id: str, amount: float) -> None:
    print(f"[PAYMENT] Obciążam klienta {customer_id} kwotą {amount} PLN")


def reserve_stock(order_id: str) -> None:
    print(f"[WAREHOUSE] Rezerwuję towar dla zamówienia {order_id}")


def refund_customer(order_id: str) -> None:
    print(f"[PAYMENT] Zwracam płatność dla zamówienia {order_id}")


class PaymentError(Exception):
    pass


class OutOfStockError(Exception):
    pass
