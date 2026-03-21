from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Nazwa produktu")
    price: float = Field(gt=0, description="Cena w PLN – musi być większa od 0")
    quantity: int = Field(default=0, ge=0, description="Ilość na stanie")


class OrderItem(BaseModel):
    quantity: int = Field(ge=1, le=1000)     # ge = greater or equal, le = less or equal
    price: float = Field(gt=0, lt=1_000_000) # gt = greater than, lt = less than
    discount: float = Field(default=0, ge=0, le=100)  # procent rabatu 0-100


class UserRegistration(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8, max_length=128)
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")


# Przykłady użycia
product = Product(name="Laptop", price=4999.99, quantity=10)
print(product)

order_item = OrderItem(quantity=5, price=29.99)
print(order_item)

user = UserRegistration(username="kacper", password="haslo1234", email="kacper@test.pl")
print(user)
