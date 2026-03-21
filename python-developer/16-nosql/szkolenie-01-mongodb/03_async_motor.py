"""
Szkolenie 1: NoSQL i MongoDB – Motor (async driver)
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


async def main():
    # Połączenie z MongoDB (asynchroniczne)
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["devs_mentoring"]
    courses = db["courses"]

    # Dodanie dokumentu
    result = await courses.insert_one({
        "name": "Async Python",
        "language": "Python",
        "no_slots": 10
    })
    print(f"Dodano: {result.inserted_id}")

    # Wyszukanie dokumentów
    async for course in courses.find({"language": "Python"}):
        print(course["name"])

    # Zliczanie
    count = await courses.count_documents({})
    print(f"Łączna liczba kursów: {count}")


asyncio.run(main())
