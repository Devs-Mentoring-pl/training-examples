from typing import Annotated

from fastapi import Depends, HTTPException, status

from .auth0 import CurrentUser, TokenPayload


def require_permissions(*required_permissions: str):
    """
    Factory zwracająca FastAPI dependency sprawdzającą permissions.

    Użycie:
        @router.get("/", dependencies=[Depends(require_permissions("read:docs"))])
        async def list_docs(): ...
    """
    async def check_permissions(current_user: CurrentUser) -> TokenPayload:
        granted = set(current_user.permissions)
        missing = set(required_permissions) - granted
        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Brak uprawnień: {', '.join(sorted(missing))}",
            )
        return current_user
    return check_permissions


def require_roles(*required_roles: str):
    """
    Dependency sprawdzająca, czy użytkownik ma jedną z wymaganych ról.

    Użycie:
        @router.get("/admin", dependencies=[Depends(require_roles("admin"))])
        async def admin_panel(): ...
    """
    async def check_roles(current_user: CurrentUser) -> TokenPayload:
        if not any(role in current_user.roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Wymagana rola: {' lub '.join(required_roles)}",
            )
        return current_user
    return check_roles


# Gotowe dependency dla typowych uprawnień
ReadDocuments = Annotated[TokenPayload, Depends(require_permissions("read:documents"))]
WriteDocuments = Annotated[TokenPayload, Depends(require_permissions("write:documents"))]
