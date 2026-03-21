from pydantic import BaseModel, EmailStr, ConfigDict


# --- Schematy dla Task ---

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    is_done: bool = False


class TaskCreate(TaskBase):
    """Schemat do tworzenia zadania – bez id, bez owner_id."""
    pass


class TaskUpdate(BaseModel):
    """Schemat do aktualizacji – wszystkie pola opcjonalne."""
    title: str | None = None
    description: str | None = None
    is_done: bool | None = None


class TaskResponse(TaskBase):
    """Schemat odpowiedzi – zawiera id i owner_id."""
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


# --- Schematy dla User ---

class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    """Schemat do tworzenia użytkownika."""
    pass


class UserResponse(UserBase):
    """Schemat odpowiedzi – z id, aktywnością i listą zadań."""
    id: int
    is_active: bool
    tasks: list[TaskResponse] = []

    model_config = ConfigDict(from_attributes=True)
