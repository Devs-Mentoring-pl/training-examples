"""
Szkolenie 9 Dataclasses i Enum - Przyklad 4
Enum - eliminacja magicznych stringow, IntEnum, StrEnum, auto().
"""

from enum import Enum, IntEnum, auto


# ========== Podstawowy Enum ==========

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


print("=== Podstawowy Enum ===")
# Dostep po nazwie
print(f"Color.RED:       {Color.RED}")
print(f"Color.RED.name:  {Color.RED.name}")
print(f"Color.RED.value: {Color.RED.value}")

# Dostep po wartosci
print(f"Color(2):        {Color(2)}")

# Dostep po nazwie (string)
print(f'Color["BLUE"]:   {Color["BLUE"]}')

# Iteracja
print("\nIteracja po Color:")
for color in Color:
    print(f"  {color.name} = {color.value}")

# Porownywanie
print(f"\nColor.RED is Color.RED:  {Color.RED is Color.RED}")     # True
print(f"Color.RED == Color.RED: {Color.RED == Color.RED}")        # True
print(f"Color.RED == 1:         {Color.RED == 1}")                # False!

# Singleton
a = Color.RED
b = Color.RED
print(f"a is b (singleton):     {a is b}")  # True


# ========== IntEnum - wartosc jako int ==========

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


print("\n=== IntEnum ===")
print(f"Priority.HIGH == 3:              {Priority.HIGH == 3}")         # True
print(f"Priority.HIGH > Priority.LOW:    {Priority.HIGH > Priority.LOW}")  # True
print(f"Priority.HIGH + 1:               {Priority.HIGH + 1}")           # 4


# ========== auto() ==========

class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


print("\n=== auto() ===")
for d in Direction:
    print(f"  {d.name} = {d.value}")


# Nadpisanie _generate_next_value_
class LowerCaseEnum(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()


class Status(LowerCaseEnum):
    ACTIVE = auto()
    INACTIVE = auto()
    PENDING = auto()


print("\n=== auto() z lowercase ===")
for s in Status:
    print(f"  {s.name} -> value: '{s.value}'")
