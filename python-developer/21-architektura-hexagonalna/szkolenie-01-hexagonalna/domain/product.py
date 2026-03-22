from dataclasses import dataclass


@dataclass
class Product:
    """Encja produktu – czysta Python, zero zależności zewnętrznych."""
    id: int
    name: str
    price: float
    stock: int

    def has_sufficient_stock(self, quantity: int) -> bool:
        """Sprawdza, czy na stanie jest wystarczająca ilość towaru."""
        return self.stock >= quantity

    def reduce_stock(self, quantity: int) -> None:
        """Zmniejsza stan magazynowy o podaną ilość."""
        if not self.has_sufficient_stock(quantity):
            raise ValueError(
                f"Niewystarczający stan magazynowy: dostępne {self.stock}, "
                f"żądane {quantity}"
            )
        self.stock -= quantity
