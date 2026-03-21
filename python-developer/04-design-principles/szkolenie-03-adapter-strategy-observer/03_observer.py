"""
Observer - system zdarzeń.

Wzorzec Observer definiuje zależność jeden-do-wielu między obiektami.
Gdy jeden obiekt (publisher/subject) zmienia stan, wszystkie zależne
obiekty (subscribers/observers) zostają automatycznie powiadomione.
"""

from abc import ABC, abstractmethod


class EventManager:
    """Publisher - zarządza subskrypcjami i powiadomieniami"""

    def __init__(self):
        self._subscribers: dict[str, list] = {}

    def subscribe(self, event_type: str, listener: "EventListener"):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(listener)
        print(f"  + {listener.__class__.__name__} subskrybuje '{event_type}'")

    def unsubscribe(self, event_type: str, listener: "EventListener"):
        self._subscribers[event_type].remove(listener)
        print(f"  - {listener.__class__.__name__} wypisany z '{event_type}'")

    def notify(self, event_type: str, data: dict):
        print(f"\n>> Zdarzenie: '{event_type}'")
        for listener in self._subscribers.get(event_type, []):
            listener.update(event_type, data)


class EventListener(ABC):
    """Interfejs obserwatora"""

    @abstractmethod
    def update(self, event_type: str, data: dict):
        pass


class EmailNotifier(EventListener):
    def update(self, event_type: str, data: dict):
        print(f"   [Email] Wysyłam maila o: {event_type}, dane: {data}")


class LogListener(EventListener):
    def update(self, event_type: str, data: dict):
        print(f"   [Log] Zapisuję do logów: {event_type}, dane: {data}")


class SlackNotifier(EventListener):
    def update(self, event_type: str, data: dict):
        print(f"   [Slack] Powiadomienie: {event_type}, dane: {data}")


if __name__ == "__main__":
    # Konfiguracja systemu
    manager = EventManager()

    email = EmailNotifier()
    log = LogListener()
    slack = SlackNotifier()

    # Subskrypcje - kto co nasłuchuje
    manager.subscribe("user_registered", email)
    manager.subscribe("user_registered", log)
    manager.subscribe("order_placed", email)
    manager.subscribe("order_placed", slack)

    # Zdarzenia w aplikacji
    manager.notify("user_registered", {"name": "Jan", "email": "jan@example.com"})
    manager.notify("order_placed", {"order_id": 42, "total": 199.99})

    # Wypisanie się ze subskrypcji
    manager.unsubscribe("user_registered", log)
    manager.notify("user_registered", {"name": "Anna", "email": "anna@example.com"})
