from abc import ABC, abstractmethod
from typing import Optional
from domain.order import Order


class OrderRepository(ABC):
    """Port wyjściowy – umowa na dostęp do danych zamówień."""

    @abstractmethod
    def save(self, order: Order) -> Order:
        """Zapisuje zamówienie i zwraca je z przypisanym ID."""
        ...

    @abstractmethod
    def find_by_id(self, order_id: int) -> Optional[Order]:
        """Zwraca zamówienie po ID lub None, jeśli nie istnieje."""
        ...

    @abstractmethod
    def find_by_user(self, user_id: int) -> list[Order]:
        """Zwraca wszystkie zamówienia danego użytkownika."""
        ...
