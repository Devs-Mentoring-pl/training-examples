from pydantic import BaseModel, Field
from typing import Optional


class Address(BaseModel):
    street: str = Field(min_length=1)
    city: str = Field(min_length=1)
    zip_code: str = Field(pattern=r"^\d{2}-\d{3}$")  # format polskiego kodu pocztowego
    country: str = Field(default="Polska")


class User(BaseModel):
    name: str
    email: str
    address: Address             # zagnieżdżony model – wymagany
    billing_address: Optional[Address] = None  # zagnieżdżony model – opcjonalny


class Item(BaseModel):
    name: str
    quantity: int = Field(ge=1)
    price: float = Field(gt=0)


class Order(BaseModel):
    customer_name: str
    items: list[Item]  # lista zagnieżdżonych modeli
    notes: str = ""


# Przykłady użycia
user = User(
    name="Kacper",
    email="kacper@devs-mentoring.pl",
    address=Address(
        street="Marszałkowska 1",
        city="Warszawa",
        zip_code="00-001",
    ),
)
print(user)

order = Order(
    customer_name="Anna Kowalska",
    items=[
        Item(name="Laptop", quantity=1, price=4999.99),
        Item(name="Mysz", quantity=2, price=89.90),
    ],
)
print(order)
