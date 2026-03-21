"""
Szkolenie 6 Wielowatkowosc - Przyklad 4
Zapobieganie data race - synchronizacja z threading.Lock.
"""

import threading

value = 0
lock = threading.Lock()


def increase_by_one():
    global value
    with lock:
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

    print(value)  # Teraz zawsze 200000


if __name__ == "__main__":
    main()
