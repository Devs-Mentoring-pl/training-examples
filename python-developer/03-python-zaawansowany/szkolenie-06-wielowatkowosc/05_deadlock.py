"""
Szkolenie 6 Wielowatkowosc - Przyklad 5
Deadlock - program zawiesza sie przy podwojnym acquire() bez release().
UWAGA: Program zawiesi sie celowo! Uzyj Ctrl+C aby przerwac.
"""

import threading


def do_deadlock():
    lock = threading.Lock()
    print("Before first acquire")
    lock.acquire()
    print("Before second acquire")
    lock.acquire()  # Tu program sie zawiesi!
    lock.release()
    print("You'll never come over here!")


def main():
    do_deadlock()


if __name__ == "__main__":
    main()
