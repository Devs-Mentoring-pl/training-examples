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


# Gotowe dependency dla typowych uprawnień
ReadDocuments = Annotated[TokenPayload, Depends(require_permissions("read:documents"))]
WriteDocuments = Annotated[TokenPayload, Depends(require_permissions("write:documents"))]
