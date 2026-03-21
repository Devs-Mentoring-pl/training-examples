"""
Szkolenie 9 Dataclasses i Enum - Przyklad 1
Podstawy @dataclass - eliminacja boilerplate'u.
"""

from dataclasses import dataclass


# ========== Zwykla klasa vs @dataclass ==========

# Zwykla klasa - duzo powtorzen
class UserOld:
    def __init__(self, name: str, email: str, age: int, active: bool = True):
        self.name = name
        self.email = email
        self.age = age
        self.active = active

    def __repr__(self) -> str:
        return (
            f"UserOld(name={self.name!r}, email={self.email!r}, "
            f"age={self.age}, active={self.active})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserOld):
            return NotImplemented
        return (
            self.name == other.name
            and self.email == other.email
            and self.age == other.age
            and self.active == other.active
        )


# Dataclass - 5 linii, ten sam efekt
@dataclass
class User:
    name: str
    email: str
    age: int
    active: bool = True


print("=== Porownanie: zwykla klasa vs @dataclass ===")

u_old = UserOld("Jan", "jan@example.com", 30)
u_new = User("Jan", "jan@example.com", 30)

print(f"UserOld: {u_old}")
print(f"User:    {u_new}")


# __eq__ dziala automatycznie
u_new2 = User("Jan", "jan@example.com", 30)
print(f"\nPorownanie == : {u_new == u_new2}")   # True


# ========== Wiecej dataclass ==========

@dataclass
class Product:
    name: str
    price: float
    quantity: int


print("\n=== Product dataclass ===")
p1 = Product(name="Laptop", price=3999.99, quantity=5)
p2 = Product(name="Laptop", price=3999.99, quantity=5)

print(f"p1: {p1}")
print(f"p2: {p2}")
print(f"p1 == p2: {p1 == p2}")   # True - porownanie po wartosciach
