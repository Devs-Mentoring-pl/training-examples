from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/users",
    tags=["Użytkownicy"],
)

fake_users_db = {
    1: {"name": "Anna", "email": "anna@example.com"},
    2: {"name": "Bartek", "email": "bartek@example.com"},
}


@router.get("/")
def get_users():
    return list(fake_users_db.values())


@router.get("/{user_id}")
def get_user(user_id: int):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="Użytkownik nie znaleziony")
    return fake_users_db[user_id]
