# application.py – przykład mockowania całej klasy

import time


class MyClass:
    def __init__(self, some_parameter) -> None:
        self.some_value = some_parameter
        time.sleep(6)

    def get_something(self) -> str:
        return 'Hello'
