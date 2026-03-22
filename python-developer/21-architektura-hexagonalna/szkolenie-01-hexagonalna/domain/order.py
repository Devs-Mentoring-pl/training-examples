from dataclasses import dataclass
from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass
class Order:
    """Encja zamówienia – czysta Python, zero zależności zewnętrznych."""
    user_id: int
    product_id: int
    quantity: int
    total_price: float
    status: OrderStatus = OrderStatus.PENDING
    id: int | None = None

    def confirm(self) -> None:
        """Potwierdza zamówienie."""
        if self.status != OrderStatus.PENDING:
            raise ValueError(f"Nie można potwierdzić zamówienia w statusie {self.status}")
        self.status = OrderStatus.CONFIRMED

    def cancel(self) -> None:
        """Anuluje zamówienie."""
        if self.status == OrderStatus.CANCELLED:
            raise ValueError("Zamówienie jest już anulowane")
        self.status = OrderStatus.CANCELLED
