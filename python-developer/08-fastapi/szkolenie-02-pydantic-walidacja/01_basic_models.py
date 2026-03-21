from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int
    email: str
    is_active: bool = True  # pole z wartością domyślną


# ✅ Poprawne dane – Pydantic je zaakceptuje
user = User(name="Kacper", age=28, email="kacper@devs-mentoring.pl")
print(user.name)       # Kacper
print(user.is_active)  # True (wartość domyślna)

# ✅ Pydantic potrafi konwertować typy (coercion)
user2 = User(name="Anna", age="25", email="anna@test.pl")
print(user2.age)       # 25 (int, nie str!)
print(type(user2.age)) # <class 'int'>

# model_validate() – walidacja ze słownika
data = {"name": "Kacper", "age": 28, "email": "kacper@devs-mentoring.pl"}
user = User.model_validate(data)
print(user)
# name='Kacper' age=28 email='kacper@devs-mentoring.pl' is_active=True

# model_validate_json() – walidacja z JSON stringa
json_string = '{"name": "Kacper", "age": 28, "email": "kacper@devs-mentoring.pl"}'
user = User.model_validate_json(json_string)

# model_dump() – serializacja do słownika
user = User(name="Kacper", age=28, email="kacper@devs-mentoring.pl")

# Do słownika
user_dict = user.model_dump()
print(user_dict)
# {'name': 'Kacper', 'age': 28, 'email': 'kacper@devs-mentoring.pl', 'is_active': True}

# Do JSON-a (string)
user_json = user.model_dump_json()
print(user_json)
# '{"name":"Kacper","age":28,"email":"kacper@devs-mentoring.pl","is_active":true}'

# Możesz wybrać, które pola uwzględnić
user_dict = user.model_dump(include={"name", "email"})
print(user_dict)  # {'name': 'Kacper', 'email': 'kacper@devs-mentoring.pl'}

# ...albo które wykluczyć
user_dict = user.model_dump(exclude={"is_active"})
print(user_dict)  # {'name': 'Kacper', 'age': 28, 'email': 'kacper@devs-mentoring.pl'}
