"""
Szkolenie 1: NoSQL i MongoDB – Aggregation Pipeline z pymongo
"""

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["devs_mentoring"]
courses = db["courses"]

# Przygotowanie danych testowych
courses.delete_many({})
courses.insert_many([
    {"name": "Python for beginners", "language": "Python", "no_slots": 15, "slots_taken": 5},
    {"name": "Python advanced", "language": "Python", "no_slots": 20, "slots_taken": 18},
    {"name": "Java essentials", "language": "Java", "no_slots": 25, "slots_taken": 10},
    {"name": "Java spring boot", "language": "Java", "no_slots": 30, "slots_taken": 28},
    {"name": "Go fundamentals", "language": "Go", "no_slots": 10, "slots_taken": 3},
    {"name": "JavaScript essentials", "language": "JavaScript", "no_slots": 25, "slots_taken": 18},
])

# --- Aggregation Pipeline ---

# Przykład 1: Grupowanie kursów po języku z liczeniem
pipeline_group = [
    {
        "$group": {
            "_id": "$language",
            "total_courses": {"$sum": 1},
            "avg_slots": {"$avg": "$no_slots"},
            "total_taken": {"$sum": "$slots_taken"},
        }
    },
    {"$sort": {"total_courses": -1}},
]

print("=== Grupowanie po języku ===")
for doc in courses.aggregate(pipeline_group):
    print(f"  {doc['_id']}: {doc['total_courses']} kursów, "
          f"śr. slotów: {doc['avg_slots']:.0f}, zajętych: {doc['total_taken']}")

# Przykład 2: Filtrowanie + projekcja (odpowiednik SELECT ... WHERE)
pipeline_filter = [
    {"$match": {"slots_taken": {"$gte": 10}}},
    {"$project": {"name": 1, "language": 1, "fill_rate": {
        "$multiply": [{"$divide": ["$slots_taken", "$no_slots"]}, 100]
    }}},
    {"$sort": {"fill_rate": -1}},
]

print("\n=== Kursy z >= 10 zajętymi slotami (fill rate) ===")
for doc in courses.aggregate(pipeline_filter):
    print(f"  {doc['name']} ({doc['language']}): {doc['fill_rate']:.1f}%")

# Przykład 3: $match + $group + $sort
pipeline_popular = [
    {"$match": {"slots_taken": {"$gt": 5}}},
    {
        "$group": {
            "_id": "$language",
            "courses": {"$push": "$name"},
            "max_taken": {"$max": "$slots_taken"},
        }
    },
    {"$sort": {"max_taken": -1}},
]

print("\n=== Popularne języki (kursy z > 5 zapisanymi) ===")
for doc in courses.aggregate(pipeline_popular):
    print(f"  {doc['_id']}: max zajętych={doc['max_taken']}, kursy={doc['courses']}")
