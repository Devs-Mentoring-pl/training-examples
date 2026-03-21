"""
Szkolenie 7 Async/Await - Przyklad 4
Event loop w akcji - zadania koncza sie w kolejnosci od najkrotszego.
"""

import asyncio


async def task(name, seconds):
    print(f"[{name}] Rozpoczynam (będę czekać {seconds}s)")
    await asyncio.sleep(seconds)
    print(f"[{name}] Zakończone!")


async def main():
    print("=== Event loop w akcji ===")
    await asyncio.gather(
        task("A", 3),
        task("B", 1),
        task("C", 2),
    )


asyncio.run(main())
