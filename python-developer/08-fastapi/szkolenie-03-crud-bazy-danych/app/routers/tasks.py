from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import Task, User
from app.schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/users/{user_id}/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: int,
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
):
    """Tworzy zadanie dla danego użytkownika."""
    # Sprawdź, czy użytkownik istnieje
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Użytkownik o id {user_id} nie istnieje",
        )

    new_task = Task(**task_data.model_dump(), owner_id=user_id)
    db.add(new_task)
    await db.flush()
    await db.refresh(new_task)
    return new_task


@router.get("/", response_model=list[TaskResponse])
async def read_tasks(user_id: int, db: AsyncSession = Depends(get_db)):
    """Zwraca wszystkie zadania danego użytkownika."""
    query = select(Task).where(Task.owner_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: int,
    task_id: int,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Aktualizuje zadanie – tylko przesłane pola."""
    query = select(Task).where(Task.id == task_id, Task.owner_id == user_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zadanie nie istnieje lub nie należy do tego użytkownika",
        )

    # exclude_unset=True – pomija pola, które klient nie przesłał
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    await db.flush()
    await db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: int,
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Usuwa zadanie."""
    query = select(Task).where(Task.id == task_id, Task.owner_id == user_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zadanie nie istnieje lub nie należy do tego użytkownika",
        )

    await db.delete(task)
