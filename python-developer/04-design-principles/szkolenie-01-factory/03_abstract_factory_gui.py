"""
Abstract Factory - komponenty GUI dla różnych systemów operacyjnych.

Abstract Factory umożliwia tworzenie rodzin powiązanych obiektów
(np. UnixFactory produkuje UnixButton, UnixCheckbox itd.)
bez specyfikowania ich konkretnych klas.
"""

from abc import ABC


class Button(ABC):
    def render(self):
        raise NotImplementedError


class UnixButton(Button):
    def render(self):
        print("Rendering an Unix button...")


class WindowsButton(Button):
    def render(self):
        print("Rendering a Windows button...")


class GUIFactory(ABC):
    def create_button(self):
        raise NotImplementedError


class UnixFactory(GUIFactory):
    def create_button(self) -> UnixButton:
        return UnixButton()


class WindowsFactory(GUIFactory):
    def create_button(self) -> WindowsButton:
        return WindowsButton()


def main():
    config = {"Windows": WindowsFactory, "Unix": UnixFactory}

    system_name = "Windows"
    factory = config.get(system_name)()
    button = factory.create_button()
    button.render()

    system_name = "Unix"
    factory = config.get(system_name)()
    button = factory.create_button()
    button.render()


if __name__ == "__main__":
    main()
