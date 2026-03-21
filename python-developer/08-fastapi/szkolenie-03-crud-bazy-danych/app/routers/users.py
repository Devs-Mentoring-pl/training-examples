from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


# CREATE – POST /users/
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Tworzy nowego użytkownika."""
    # Sprawdź, czy email nie jest już zajęty
    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Użytkownik z emailem {user_data.email} już istnieje",
        )

    new_user = User(**user_data.model_dump())
    db.add(new_user)
    await db.flush()       # wymusza nadanie id bez commitowania
    await db.refresh(new_user)  # odświeża obiekt z bazy (m.in. id, created_at)
    return new_user


# READ ALL – GET /users/
@router.get("/", response_model=list[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Zwraca listę użytkowników z paginacją."""
    query = (
        select(User)
        .options(selectinload(User.tasks))  # eager loading – unikamy N+1
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    users = result.scalars().all()
    return users


# READ ONE – GET /users/{user_id}
@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Zwraca użytkownika po ID."""
    query = select(User).options(selectinload(User.tasks)).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Użytkownik o id {user_id} nie istnieje",
        )
    return user


# UPDATE – PUT /users/{user_id}
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """Aktualizuje dane użytkownika."""
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Użytkownik o id {user_id} nie istnieje",
        )

    # Aktualizacja atrybutów
    for field, value in user_data.model_dump().items():
        setattr(user, field, value)

    await db.flush()
    await db.refresh(user)
    return user


# DELETE – DELETE /users/{user_id}
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Usuwa użytkownika."""
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Użytkownik o id {user_id} nie istnieje",
        )

    await db.delete(user)
