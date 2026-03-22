from dataclasses import dataclass

from domain.order import Order
from domain.exceptions import ProductNotFoundError, InsufficientStockError
from ports.order_repository import OrderRepository
from ports.product_repository import ProductRepository
from ports.notification_service import NotificationService


@dataclass
class PlaceOrderCommand:
    """Dane wejściowe dla use case'u – prosty obiekt danych."""
    user_id: int
    user_email: str
    product_id: int
    quantity: int


@dataclass
class PlaceOrderResult:
    """Dane wyjściowe use case'u."""
    order_id: int
    total_price: float
    status: str


class PlaceOrderUseCase:
    """
    Use case: złóż zamówienie.

    Zawiera czystą logikę biznesową. Nie wie nic o HTTP, bazie danych
    ani emailach – komunikuje się z nimi wyłącznie przez porty.
    """

    def __init__(
        self,
        order_repository: OrderRepository,
        product_repository: ProductRepository,
        notification_service: NotificationService,
    ) -> None:
        self._order_repo = order_repository
        self._product_repo = product_repository
        self._notification = notification_service

    def execute(self, command: PlaceOrderCommand) -> PlaceOrderResult:
        """Wykonuje logikę biznesową złożenia zamówienia."""

        product = self._product_repo.find_by_id(command.product_id)
        if product is None:
            raise ProductNotFoundError(command.product_id)

        if not product.has_sufficient_stock(command.quantity):
            raise InsufficientStockError(
                product_id=command.product_id,
                available=product.stock,
                requested=command.quantity,
            )

        total_price = product.price * command.quantity

        order = Order(
            user_id=command.user_id,
            product_id=command.product_id,
            quantity=command.quantity,
            total_price=total_price,
        )
        order.confirm()

        product.reduce_stock(command.quantity)
        self._product_repo.update_stock(command.product_id, product.stock)

        saved_order = self._order_repo.save(order)

        self._notification.send_order_confirmation(
            user_email=command.user_email,
            order_id=saved_order.id,
            total=total_price,
        )

        return PlaceOrderResult(
            order_id=saved_order.id,
            total_price=total_price,
            status=saved_order.status.value,
        )
