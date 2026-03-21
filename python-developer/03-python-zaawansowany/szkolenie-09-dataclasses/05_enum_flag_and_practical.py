"""
Szkolenie 9 Dataclasses i Enum - Przyklad 5
Flag (uprawnienia bitowe), Enum+Dataclass, maszyna stanow.
"""

from dataclasses import dataclass
from enum import Enum, Flag, IntEnum, IntFlag, auto


# ========== Flag - uprawnienia bitowe ==========

class Permission(Flag):
    READ = auto()      # 1
    WRITE = auto()     # 2
    EXECUTE = auto()   # 4
    DELETE = auto()    # 8

    # Predefiniowane kombinacje
    VIEWER = READ
    EDITOR = READ | WRITE
    ADMIN = READ | WRITE | EXECUTE | DELETE


def check_access(user_perms: Permission, required: Permission) -> bool:
    return required in user_perms


print("=== Flag: uprawnienia ===")
editor = Permission.EDITOR
print(f"EDITOR = {editor}")
print(f"  READ:    {check_access(editor, Permission.READ)}")     # True
print(f"  WRITE:   {check_access(editor, Permission.WRITE)}")    # True
print(f"  DELETE:  {check_access(editor, Permission.DELETE)}")   # False

admin = Permission.ADMIN
print(f"\nADMIN = {admin}")
print(f"  DELETE:  {check_access(admin, Permission.DELETE)}")    # True


# ========== Maszyna stanow - statusy zamowienia ==========

class OrderStatus(Enum):
    DRAFT = auto()
    PENDING = auto()
    CONFIRMED = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()

    def can_transition_to(self, new_status: "OrderStatus") -> bool:
        allowed = {
            OrderStatus.DRAFT: {OrderStatus.PENDING, OrderStatus.CANCELLED},
            OrderStatus.PENDING: {OrderStatus.CONFIRMED, OrderStatus.CANCELLED},
            OrderStatus.CONFIRMED: {OrderStatus.SHIPPED, OrderStatus.CANCELLED},
            OrderStatus.SHIPPED: {OrderStatus.DELIVERED},
            OrderStatus.DELIVERED: set(),
            OrderStatus.CANCELLED: set(),
        }
        return new_status in allowed[self]


print("\n=== Maszyna stanow: zamowienie ===")
order = OrderStatus.PENDING
transitions = [
    OrderStatus.CONFIRMED,
    OrderStatus.DELIVERED,
    OrderStatus.CANCELLED,
]

for target in transitions:
    result = order.can_transition_to(target)
    print(f"  {order.name} -> {target.name}: {'OK' if result else 'ZABRONIONE'}")


# ========== Enum + Dataclass ==========

class Role(Enum):
    ADMIN = auto()
    EDITOR = auto()
    VIEWER = auto()


@dataclass
class User:
    name: str
    email: str
    role: Role = Role.VIEWER

    def has_permission(self, required_role: Role) -> bool:
        role_hierarchy = {
            Role.VIEWER: 0,
            Role.EDITOR: 1,
            Role.ADMIN: 2,
        }
        return role_hierarchy[self.role] >= role_hierarchy[required_role]


print("\n=== Enum + Dataclass: User z rola ===")
admin = User("Kacper", "kacper@devs-mentoring.pl", Role.ADMIN)
viewer = User("Jan", "jan@example.com")

print(f"admin: {admin}")
print(f"  has EDITOR perm: {admin.has_permission(Role.EDITOR)}")   # True
print(f"viewer: {viewer}")
print(f"  has ADMIN perm: {viewer.has_permission(Role.ADMIN)}")    # False
print(f"  role: {viewer.role}")


# ========== HTTP Status Codes ==========

class HttpStatus(IntEnum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

    @property
    def is_success(self) -> bool:
        return 200 <= self.value < 300

    @property
    def is_client_error(self) -> bool:
        return 400 <= self.value < 500


print("\n=== HttpStatus z property ===")
for status in [HttpStatus.OK, HttpStatus.NOT_FOUND, HttpStatus.INTERNAL_SERVER_ERROR]:
    print(f"  {status.name} ({status.value}): "
          f"success={status.is_success}, client_error={status.is_client_error}")
