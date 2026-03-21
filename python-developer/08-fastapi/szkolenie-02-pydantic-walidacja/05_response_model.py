from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class UserInDB(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str  # tego NIE chcemy zwracać!
    is_active: bool


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    # Symulacja pobrania z bazy danych
    user = UserInDB(
        id=user_id,
        username="kacper",
        email="kacper@devs-mentoring.pl",
        hashed_password="$2b$12$abc...",
        is_active=True,
    )
    return user  # FastAPI automatycznie odfiltruje hashed_password!
