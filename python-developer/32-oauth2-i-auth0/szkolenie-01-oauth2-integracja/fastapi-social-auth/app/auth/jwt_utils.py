import os
from datetime import datetime, timedelta, timezone

import jwt

SECRET_KEY = os.environ.get("SECRET_KEY", "zmien-to-w-produkcji")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Tworzy JWT z podanymi danymi i czasem wygasnięcia."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Dekoduje i weryfikuje JWT. Rzuca wyjątek jeśli token jest nieprawidłowy."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Nieprawidłowy token: {e}")
