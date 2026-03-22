import sys
import os

# Dodaj katalog główny projektu do PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from application.place_order import PlaceOrderCommand, PlaceOrderUseCase
from adapters.in_memory_order_repository import InMemoryOrderRepository
from adapters.in_memory_product_repository import InMemoryProductRepository
from adapters.fake_notification_service import FakeNotificationService
from domain.product import Product
from domain.order import OrderStatus
from domain.exceptions import ProductNotFoundError, InsufficientStockError


class TestPlaceOrderUseCase:
    """Testy use case'u złożenia zamówienia – bez żadnej bazy danych."""

    def setup_method(self) -> None:
        """Przygotowanie testów – in-memory adaptery zamiast prawdziwych."""
        self.order_repo = InMemoryOrderRepository()
        self.product_repo = InMemoryProductRepository()
        self.notification_service = FakeNotificationService()

        self.product_repo.add(Product(
            id=1,
            name="Klawiatura mechaniczna",
            price=299.99,
            stock=10,
        ))

        self.use_case = PlaceOrderUseCase(
            order_repository=self.order_repo,
            product_repository=self.product_repo,
            notification_service=self.notification_service,
        )

    def test_place_order_successfully(self) -> None:
        """Pomyślne złożenie zamówienia."""
        command = PlaceOrderCommand(
            user_id=42,
            user_email="jan@example.com",
            product_id=1,
            quantity=2,
        )

        result = self.use_case.execute(command)

        assert result.order_id is not None
        assert result.total_price == 599.98
        assert result.status == OrderStatus.CONFIRMED.value

        product = self.product_repo.find_by_id(1)
        assert product.stock == 8

        assert len(self.notification_service.sent_notifications) == 1
        notification = self.notification_service.sent_notifications[0]
        assert notification["email"] == "jan@example.com"
        assert notification["order_id"] == result.order_id

    def test_place_order_product_not_found(self) -> None:
        """Próba zamówienia nieistniejącego produktu."""
        command = PlaceOrderCommand(
            user_id=42,
            user_email="jan@example.com",
            product_id=999,
            quantity=1,
        )

        with pytest.raises(ProductNotFoundError) as exc_info:
            self.use_case.execute(command)

        assert exc_info.value.product_id == 999

    def test_place_order_insufficient_stock(self) -> None:
        """Próba zamówienia większej ilości niż dostępna."""
        command = PlaceOrderCommand(
            user_id=42,
            user_email="jan@example.com",
            product_id=1,
            quantity=100,
        )

        with pytest.raises(InsufficientStockError) as exc_info:
            self.use_case.execute(command)

        assert exc_info.value.available == 10
        assert exc_info.value.requested == 100

    def test_no_notification_sent_on_failure(self) -> None:
        """Przy błędzie nie wysyłamy powiadomień."""
        command = PlaceOrderCommand(
            user_id=42,
            user_email="jan@example.com",
            product_id=999,
            quantity=1,
        )

        with pytest.raises(ProductNotFoundError):
            self.use_case.execute(command)

        assert len(self.notification_service.sent_notifications) == 0

    def test_stock_not_reduced_on_failure(self) -> None:
        """Przy błędzie stan magazynowy nie powinien się zmienić."""
        initial_stock = self.product_repo.find_by_id(1).stock

        command = PlaceOrderCommand(
            user_id=42,
            user_email="jan@example.com",
            product_id=1,
            quantity=100,
        )

        with pytest.raises(InsufficientStockError):
            self.use_case.execute(command)

        assert self.product_repo.find_by_id(1).stock == initial_stock
