class DomainException(Exception):
    """Bazowy wyjątek domenowy."""
    pass


class ProductNotFoundError(DomainException):
    """Produkt nie został znaleziony."""
    def __init__(self, product_id: int) -> None:
        super().__init__(f"Produkt o ID {product_id} nie istnieje")
        self.product_id = product_id


class InsufficientStockError(DomainException):
    """Niewystarczający stan magazynowy."""
    def __init__(self, product_id: int, available: int, requested: int) -> None:
        super().__init__(
            f"Produkt {product_id}: dostępne {available}, żądane {requested}"
        )
        self.product_id = product_id
        self.available = available
        self.requested = requested


class OrderNotFoundError(DomainException):
    """Zamówienie nie zostało znalezione."""
    def __init__(self, order_id: int) -> None:
        super().__init__(f"Zamówienie o ID {order_id} nie istnieje")
        self.order_id = order_id
