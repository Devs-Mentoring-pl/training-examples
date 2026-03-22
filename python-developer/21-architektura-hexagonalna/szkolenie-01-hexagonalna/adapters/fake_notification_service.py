from ports.notification_service import NotificationService


class FakeNotificationService(NotificationService):
    """Adapter – fałszywy serwis powiadomień do testów. Zbiera wysłane wiadomości."""

    def __init__(self) -> None:
        self.sent_notifications: list[dict] = []

    def send_order_confirmation(self, user_email: str, order_id: int, total: float) -> None:
        self.sent_notifications.append({
            "email": user_email,
            "order_id": order_id,
            "total": total,
        })
