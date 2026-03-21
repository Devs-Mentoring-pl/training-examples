"""
Szkolenie 8 Type Hints - Przyklad 4
Type hints w klasach - atrybuty, metody, wlasne klasy jako typy.
"""

from dataclasses import dataclass


# ========== Klasa z type hints ==========

class User:
    def __init__(self, name: str, age: int, email: str | None = None) -> None:
        self.name: str = name
        self.age: int = age
        self.email: str | None = email

    def greet(self) -> str:
        return f"Czesc, jestem {self.name}!"

    def is_adult(self) -> bool:
        return self.age >= 18


print("=== Klasa User z type hints ===")
u1 = User("Anna", 25, "anna@example.com")
u2 = User("Bartek", 15)

print(u1.greet())
print(f"  adult: {u1.is_adult()}, email: {u1.email}")
print(u2.greet())
print(f"  adult: {u2.is_adult()}, email: {u2.email}")


# ========== Atrybuty klasy ==========

class Config:
    MAX_RETRIES: int = 3
    TIMEOUT: float = 30.0
    BASE_URL: str = "https://api.example.com"

    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key


print("\n=== Atrybuty klasy ===")
config = Config("secret-key-123")
print(f"MAX_RETRIES: {Config.MAX_RETRIES}")
print(f"TIMEOUT: {Config.TIMEOUT}")
print(f"BASE_URL: {Config.BASE_URL}")


# ========== Wlasne klasy jako typy ==========

class Product:
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def __repr__(self) -> str:
        return f"Product({self.name!r}, {self.price})"


class ShoppingCart:
    def __init__(self) -> None:
        self.items: list[Product] = []

    def add(self, product: Product) -> None:
        self.items.append(product)

    def total(self) -> float:
        return sum(item.price for item in self.items)

    def display(self) -> None:
        for item in self.items:
            print(f"  {item.name}: {item.price:.2f} PLN")
        print(f"  RAZEM: {self.total():.2f} PLN")


print("\n=== Klasy jako typy: ShoppingCart ===")
cart = ShoppingCart()
cart.add(Product("Laptop", 3999.99))
cart.add(Product("Mysz", 129.99))
cart.add(Product("Klawiatura", 249.99))
cart.display()


# ========== Dataclass z type hints ==========

@dataclass
class Point:
    x: float
    y: float
    label: str = "origin"


print("\n=== Dataclass: Point ===")
p1 = Point(1.0, 2.5, "A")
p2 = Point(3.0, 4.0)
print(f"p1: {p1}")
print(f"p2: {p2}")
