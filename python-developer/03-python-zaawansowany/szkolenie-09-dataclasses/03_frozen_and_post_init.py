"""
Szkolenie 9 Dataclasses i Enum - Przyklad 3
frozen=True (niemutowalne), __post_init__ (walidacja, pola obliczane).
"""

from dataclasses import dataclass, field, InitVar


# ========== frozen=True ==========

@dataclass(frozen=True)
class Point:
    x: float
    y: float


print("=== frozen=True: niemutowalna dataclass ===")
p = Point(x=1.0, y=2.0)
print(f"p: {p}")

try:
    p.x = 5.0
except AttributeError as e:
    print(f"Proba zmiany: {e}")


# Frozen dataclass jako klucz slownika
@dataclass(frozen=True)
class Color:
    r: int
    g: int
    b: int


palette = {
    Color(255, 0, 0): "czerwony",
    Color(0, 255, 0): "zielony",
    Color(0, 0, 255): "niebieski",
}

print(f"\npalette[Color(255,0,0)] = '{palette[Color(255, 0, 0)]}'")


# ========== __post_init__ - walidacja ==========

@dataclass
class Temperature:
    celsius: float

    def __post_init__(self):
        if self.celsius < -273.15:
            raise ValueError(
                f"Temperatura {self.celsius} C jest ponizej zera absolutnego!"
            )


print("\n=== __post_init__: walidacja ===")
t1 = Temperature(celsius=25.0)
print(f"t1: {t1}")

try:
    t2 = Temperature(celsius=-300.0)
except ValueError as e:
    print(f"Blad walidacji: {e}")


# ========== __post_init__ + InitVar + field(init=False) ==========

@dataclass
class Invoice:
    net_price: float
    vat_rate: InitVar[float]  # argument __init__, nie pole klasy
    gross_price: float = field(init=False)  # pole obliczane

    def __post_init__(self, vat_rate: float):
        self.gross_price = round(self.net_price * (1 + vat_rate), 2)


print("\n=== InitVar + field(init=False): faktura ===")
inv = Invoice(net_price=100.0, vat_rate=0.23)
print(f"Faktura: {inv}")
print(f"Cena brutto: {inv.gross_price} PLN")


# ========== order=True - porownywanie i sortowanie ==========

@dataclass(order=True)
class Version:
    major: int
    minor: int
    patch: int


print("\n=== order=True: sortowanie wersji ===")
v1 = Version(1, 0, 0)
v2 = Version(2, 1, 0)
v3 = Version(1, 5, 3)

print(f"v1 < v2: {v1 < v2}")   # True
print(f"v3 > v1: {v3 > v1}")   # True

versions = [v2, v3, v1]
print(f"Posortowane: {sorted(versions)}")
