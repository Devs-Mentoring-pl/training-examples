"""
Szkolenie 7 Async/Await - Przyklad 2
asyncio.gather() - uruchamianie wielu korutyn jednoczesnie.
"""

import asyncio


async def fetch_users():
    print("Pobieram użytkowników...")
    await asyncio.sleep(2)
    return ["Anna", "Bartek", "Celina"]


async def fetch_products():
    print("Pobieram produkty...")
    await asyncio.sleep(3)
    return ["Laptop", "Myszka", "Monitor"]


async def fetch_orders():
    print("Pobieram zamówienia...")
    await asyncio.sleep(1)
    return ["ZAM-001", "ZAM-002"]


async def main():
    # Wszystkie trzy zapytania startuja jednoczesnie
    users, products, orders = await asyncio.gather(
        fetch_users(),
        fetch_products(),
        fetch_orders(),
    )

    print(f"Użytkownicy: {users}")
    print(f"Produkty: {products}")
    print(f"Zamówienia: {orders}")


asyncio.run(main())
