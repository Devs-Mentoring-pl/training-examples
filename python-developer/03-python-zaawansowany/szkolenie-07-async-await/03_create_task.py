"""
Szkolenie 7 Async/Await - Przyklad 3
asyncio.create_task() - uruchamianie zadan w tle.
"""

import asyncio


async def long_task(name, seconds):
    print(f"[{name}] Start")
    await asyncio.sleep(seconds)
    print(f"[{name}] Koniec")
    return f"Wynik z {name}"


async def main():
    # Tworzymy taski - korutyny zaczynaja sie wykonywac w tle
    task1 = asyncio.create_task(long_task("Zadanie A", 3))
    task2 = asyncio.create_task(long_task("Zadanie B", 1))

    print("Taski utworzone – mogę robić inne rzeczy...")
    await asyncio.sleep(0.5)
    print("...właśnie robię inne rzeczy.")

    # Teraz czekam na wyniki
    result1 = await task1
    result2 = await task2

    print(f"Otrzymano: {result1}, {result2}")


asyncio.run(main())
