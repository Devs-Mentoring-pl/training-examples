"""
Szkolenie 6 Wielowatkowosc - Przyklad 3
Data race - niedeterministyczny wynik przy wspoldzieleniu zmiennej.
"""

import threading

value = 0


def increase_by_one():
    global value
    for i in range(100000):
        value += 1


def main():
    threads = [
        threading.Thread(target=increase_by_one),
        threading.Thread(target=increase_by_one),
    ]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(value)  # Powinno byc 200000, ale wynik jest niedeterministyczny!


if __name__ == "__main__":
    main()
