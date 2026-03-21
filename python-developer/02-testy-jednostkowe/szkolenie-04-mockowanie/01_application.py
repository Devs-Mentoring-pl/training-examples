# application.py – przykład mockowania funkcji

import time


def do_calculation(value: int) -> int:
    response = call_api()
    return response + value  # funkcja zwiększa wartość o dane z API


def call_api():
    time.sleep(10)  # symulacja długotrwałej operacji
    return 100
