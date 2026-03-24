from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI(title="User Service", version="1.0.0")

# Symulowana baza danych – w prawdziwym projekcie PostgreSQL + SQLAlchemy
users_db: dict[int, dict] = {
    1: {"id": 1, "name": "Anna Kowalska", "email": "anna@example.com", "is_active": True},
    2: {"id": 2, "name": "Jan Nowak", "email": "jan@example.com", "is_active": True},
}
next_id = 3


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint – wymagany przez Docker i load balancer."""
    return {"status": "healthy", "service": "user-service"}


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int) -> UserResponse:
    """Pobiera użytkownika po ID."""
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"Użytkownik {user_id} nie istnieje")
    return UserResponse(**user)


@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user_data: UserCreate) -> UserResponse:
    """Tworzy nowego użytkownika."""
    global next_id
    user = {
        "id": next_id,
        "name": user_data.name,
        "email": user_data.email,
        "is_active": True,
    }
    users_db[next_id] = user
    next_id += 1
    return UserResponse(**user)
