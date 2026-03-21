"""
Adapter - konwersja napięcia (gniazdko europejskie -> urządzenie amerykańskie).

Wzorzec Adapter pozwala obiektom z niekompatybilnymi interfejsami
współpracować ze sobą. Adapter "opakowuje" jeden obiekt i tłumaczy
jego interfejs na taki, jakiego oczekuje klient.
"""


class EuropeanSocket:
    """Gniazdko europejskie - 220V"""

    def provide_power(self) -> float:
        return 220.0


class USDevice:
    """Urządzenie amerykańskie - wymaga 110V"""

    def charge(self, voltage: float):
        if voltage > 130:
            print(f"Zbyt wysokie napięcie ({voltage}V)! Urządzenie może się spalić!")
        else:
            print(f"Ładowanie przy {voltage}V - OK!")


class VoltageAdapter:
    """Adapter - konwertuje 220V na 110V"""

    def __init__(self, socket: EuropeanSocket):
        self._socket = socket

    def provide_power(self) -> float:
        voltage = self._socket.provide_power()
        adapted = voltage / 2  # konwersja 220V -> 110V
        print(f"Adapter: {voltage}V -> {adapted}V")
        return adapted


if __name__ == "__main__":
    # Bez adaptera - katastrofa!
    socket = EuropeanSocket()
    device = USDevice()
    device.charge(socket.provide_power())  # 220V -> spali urządzenie!

    print()

    # Z adapterem - bezpiecznie
    adapter = VoltageAdapter(socket)
    voltage = adapter.provide_power()
    device.charge(voltage)  # 110V -> OK!
