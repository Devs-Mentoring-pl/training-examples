from ports.product_repository import ProductRepository
from domain.product import Product


class InMemoryProductRepository(ProductRepository):
    """Adapter – implementacja repozytorium produktów w pamięci (do testów)."""

    def __init__(self) -> None:
        self._products: dict[int, Product] = {}

    def add(self, product: Product) -> None:
        """Dodaje produkt do repozytorium (metoda pomocnicza do testów)."""
        self._products[product.id] = product

    def find_by_id(self, product_id: int) -> Product | None:
        return self._products.get(product_id)

    def update_stock(self, product_id: int, new_stock: int) -> None:
        product = self._products.get(product_id)
        if product:
            product.stock = new_stock
