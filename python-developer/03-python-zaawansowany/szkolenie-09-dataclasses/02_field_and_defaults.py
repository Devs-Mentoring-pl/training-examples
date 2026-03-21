"""
Szkolenie 9 Dataclasses i Enum - Przyklad 2
Domyslne wartosci, field(), mutowalne wartosci domyslne.
"""

from dataclasses import dataclass, field


# ========== Proste wartosci domyslne ==========

@dataclass
class Config:
    host: str = "localhost"
    port: int = 8080
    debug: bool = False


print("=== Proste wartosci domyslne ===")
c1 = Config()
c2 = Config(host="0.0.0.0", port=443, debug=True)
print(f"Domyslna: {c1}")
print(f"Zmieniona: {c2}")


# ========== field(default_factory) - mutowalne wartosci ==========

@dataclass
class Team:
    name: str
    members: list[str] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)


print("\n=== field(default_factory) ===")
t1 = Team("Alpha")
t2 = Team("Beta")

t1.members.append("Anna")
t1.members.append("Bartek")
t2.members.append("Celina")

print(f"t1: {t1}")
print(f"t2: {t2}")
print(f"Rozne listy: {t1.members is not t2.members}")  # True


# ========== Zaawansowane uzycie field() ==========

@dataclass
class Employee:
    name: str
    salary: float
    _department: str = field(repr=False)           # ukryj w __repr__
    _internal_id: int = field(compare=False)       # ignoruj przy ==
    tags: list[str] = field(default_factory=list)  # mutowalna domyslna


print("\n=== Zaawansowane field() ===")
e1 = Employee("Jan", 8000.0, "IT", 12345)
e2 = Employee("Jan", 8000.0, "HR", 99999)  # inny dept i id

print(f"e1: {e1}")   # _department nie widoczne w repr
print(f"e2: {e2}")
print(f"e1 == e2: {e1 == e2}")  # True - _internal_id ignorowane
print(f"e1._department: {e1._department}")  # wciaz dostepne
