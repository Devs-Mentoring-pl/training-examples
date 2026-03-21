"""
Szkolenie 1: NoSQL i MongoDB – CRUD z pymongo 4.x
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from bson.objectid import ObjectId

# --- Połączenie z bazą danych ---

try:
    client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
    # Sprawdzenie, czy serwer odpowiada
    client.admin.command("ping")
    print("Połączenie z MongoDB udane!")
except ConnectionFailure:
    print("Nie udało się połączyć z serwerem MongoDB")
    exit(1)

# Wybór bazy danych (tworzy automatycznie, jeśli nie istnieje)
db = client["devs_mentoring"]

# Wybór kolekcji
courses = db["courses"]

# --- CREATE ---

# Dodanie jednego dokumentu
result = courses.insert_one({
    "name": "Python for beginners",
    "language": "Python",
    "no_slots": 15,
    "slots_taken": 5,
    "topics": ["Python", "Django", "Flask"],
    "is_activated": True
})
print(f"Dodano dokument o ID: {result.inserted_id}")

# Dodanie wielu dokumentów
result = courses.insert_many([
    {"name": "Java essentials", "language": "Java", "no_slots": 20},
    {"name": "Go fundamentals", "language": "Go", "no_slots": 10}
])
print(f"Dodano {len(result.inserted_ids)} dokumentów")

# --- READ ---

# Znalezienie jednego dokumentu
course = courses.find_one({"language": "Python"})
print(course)

# Znalezienie wielu dokumentów
for course in courses.find({"no_slots": {"$gte": 15}}):
    print(course["name"])

# Zliczanie dokumentów
count = courses.count_documents({"language": "Python"})
print(f"Kursów z Pythona: {count}")

# --- UPDATE ---

# Aktualizacja jednego dokumentu
courses.update_one(
    {"name": "Python for beginners"},
    {"$set": {"slots_taken": 10}}
)

# Aktualizacja wielu dokumentów
courses.update_many(
    {"language": "Java"},
    {"$inc": {"no_slots": 5}}
)

# --- DELETE ---

# Usunięcie jednego dokumentu
courses.delete_one({"name": "Go fundamentals"})

# Usunięcie wielu dokumentów
result = courses.delete_many({"no_slots": {"$lt": 5}})
print(f"Usunięto {result.deleted_count} dokumentów")
