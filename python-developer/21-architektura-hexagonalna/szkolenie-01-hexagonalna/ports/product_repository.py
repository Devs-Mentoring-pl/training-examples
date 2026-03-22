from abc import ABC, abstractmethod
from typing import Optional
from domain.product import Product


class ProductRepository(ABC):
    """Port wyjściowy – umowa na dostęp do danych produktów."""

    @abstractmethod
    def find_by_id(self, product_id: int) -> Optional[Product]:
        """Zwraca produkt po ID lub None, jeśli nie istnieje."""
        ...

    @abstractmethod
    def update_stock(self, product_id: int, new_stock: int) -> None:
        """Aktualizuje stan magazynowy produktu."""
        ...
