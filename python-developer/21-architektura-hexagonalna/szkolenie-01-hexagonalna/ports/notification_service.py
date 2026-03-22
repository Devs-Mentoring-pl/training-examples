from abc import ABC, abstractmethod


class NotificationService(ABC):
    """Port wyjściowy – umowa na wysyłanie powiadomień."""

    @abstractmethod
    def send_order_confirmation(self, user_email: str, order_id: int, total: float) -> None:
        """Wysyła potwierdzenie zamówienia na podany adres email."""
        ...
