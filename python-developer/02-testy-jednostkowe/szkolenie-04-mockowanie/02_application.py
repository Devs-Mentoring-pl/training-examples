# application.py – przykład mockowania metody w klasie

import time


class Data:
    def __init__(self):
        self.data = None

    def load_data(self):
        time.sleep(6)
        self.data = 'some data'


def get_data():
    data = Data()
    return data.load_data()
