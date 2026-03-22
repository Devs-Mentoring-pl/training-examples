from ports.order_repository import OrderRepository
from domain.order import Order


class InMemoryOrderRepository(OrderRepository):
    """Adapter – implementacja repozytorium w pamięci (używana w testach)."""

    def __init__(self) -> None:
        self._orders: dict[int, Order] = {}
        self._next_id: int = 1

    def save(self, order: Order) -> Order:
        order.id = self._next_id
        self._orders[self._next_id] = order
        self._next_id += 1
        return order

    def find_by_id(self, order_id: int) -> Order | None:
        return self._orders.get(order_id)

    def find_by_user(self, user_id: int) -> list[Order]:
        return [o for o in self._orders.values() if o.user_id == user_id]
