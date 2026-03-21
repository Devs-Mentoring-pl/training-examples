"""
Szkolenie 7 Async/Await - Przyklad 1
Porownanie podejscia synchronicznego i asynchronicznego.
"""

import asyncio


# Podejscie asynchroniczne - rownolegle
async def fetch_data_async(name, wait_time):
    print(f"Rozpoczynam pobieranie: {name}")
    await asyncio.sleep(wait_time)  # nieblokujace czekanie
    print(f"Zakończono pobieranie: {name}")


async def main():
    start = asyncio.get_running_loop().time()
    await asyncio.gather(
        fetch_data_async("API 1", 2),
        fetch_data_async("API 2", 2),
        fetch_data_async("API 3", 2),
    )
    print(f"Czas całkowity: {asyncio.get_running_loop().time() - start:.1f}s")  # ~2 sekundy!


asyncio.run(main())
