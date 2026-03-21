from datetime import datetime, timedelta, timezone
from typing import Callable

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

# --- Konfiguracja ---

SECRET_KEY = "twoj-super-tajny-klucz-ktory-nie-moze-byc-w-kodzie"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

app = FastAPI(title="Autentykacja i bezpieczeństwo")

# --- CORS ---

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://app.example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Hashowanie haseł ---

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashuje hasło za pomocą bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Porównuje hasło jawne z zahashowanym."""
    return pwd_context.verify(plain_password, hashed_password)


# --- Modele ---


class User(BaseModel):
    username: str
    email: str
    role: str = "user"


class UserInDB(User):
    hashed_password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# --- Symulowana baza danych ---

fake_users_db: dict[str, dict] = {
    "kacper": {
        "username": "kacper",
        "email": "kacper@devs-mentoring.pl",
        "role": "admin",
        "hashed_password": hash_password("admin123"),
    },
    "jan": {
        "username": "jan",
        "email": "jan@example.com",
        "role": "user",
        "hashed_password": hash_password("user123"),
    },
}


def get_user(db: dict, username: str) -> UserInDB | None:
    """Pobiera użytkownika z 'bazy danych'."""
    if username in db:
        return UserInDB(**db[username])
    return None


# --- Tokeny JWT ---


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Tworzy token JWT z podanymi danymi."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Tworzy refresh token z dłuższym czasem życia."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --- OAuth2 i dependency ---

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Dekoduje token i zwraca aktualnego użytkownika."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Nie udało się zweryfikować danych uwierzytelniających",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    user = get_user(fake_users_db, username)

    if user is None:
        raise credentials_exception

    return user


# --- Autoryzacja oparta na rolach ---


def require_role(required_role: str) -> Callable:
    """Tworzy dependency sprawdzający rolę użytkownika."""

    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Wymagana rola: {required_role}. Twoja rola: {current_user.role}",
            )
        return current_user

    return role_checker


def require_any_role(*roles: str) -> Callable:
    """Pozwala na dostęp użytkownikom z dowolną z podanych ról."""

    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Wymagana jedna z ról: {', '.join(roles)}",
            )
        return current_user

    return role_checker


# --- Endpointy ---


@app.post("/token", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Endpoint logowania – zwraca access i refresh token."""
    user = get_user(fake_users_db, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nieprawidłowa nazwa użytkownika lub hasło",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@app.post("/token/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """Odświeża access token na podstawie refresh tokena."""
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nieprawidłowy typ tokena",
            )

        username = payload.get("sub")
        new_access_token = create_access_token(data={"sub": username})
        new_refresh_token = create_refresh_token(data={"sub": username})

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token wygasł lub jest nieprawidłowy",
        )


@app.get("/me")
async def read_current_user(current_user: User = Depends(get_current_user)):
    """Zwraca dane zalogowanego użytkownika."""
    return current_user


@app.get("/my-items")
async def read_my_items(current_user: User = Depends(get_current_user)):
    """Przykładowy chroniony endpoint."""
    return {"owner": current_user.username, "items": ["laptop", "telefon"]}


@app.get("/admin/dashboard")
async def admin_dashboard(admin: User = Depends(require_role("admin"))):
    """Dostępny tylko dla administratorów."""
    return {"message": f"Witaj w panelu admina, {admin.username}!"}


@app.delete("/admin/users/{username}")
async def delete_user(
    username: str,
    admin: User = Depends(require_role("admin")),
):
    """Usuwanie użytkownika – tylko dla admina."""
    if username in fake_users_db:
        del fake_users_db[username]
        return {"message": f"Użytkownik {username} został usunięty"}
    raise HTTPException(status_code=404, detail="Użytkownik nie znaleziony")


@app.get("/reports")
async def view_reports(
    user: User = Depends(require_any_role("admin", "moderator")),
):
    """Dostępny dla adminów i moderatorów."""
    return {"reports": ["raport_miesięczny", "raport_dzienny"]}
