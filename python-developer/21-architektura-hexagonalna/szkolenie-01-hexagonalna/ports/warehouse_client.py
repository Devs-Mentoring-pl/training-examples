from typing import Protocol


class WarehouseClient(Protocol):
    """Port wyjściowy – umowa na komunikację z systemem magazynowym."""

    def reserve_stock(self, product_id: int, quantity: int) -> bool:
        """Rezerwuje towar w magazynie. Zwraca True jeśli sukces."""
        ...

    def release_stock(self, product_id: int, quantity: int) -> None:
        """Zwalnia zarezerwowany towar (np. przy anulowaniu zamówienia)."""
        ...
