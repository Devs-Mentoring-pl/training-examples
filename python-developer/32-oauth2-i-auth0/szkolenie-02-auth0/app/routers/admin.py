from fastapi import APIRouter, Depends

from app.auth.permissions import require_roles

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard", dependencies=[Depends(require_roles("admin"))])
async def admin_dashboard():
    """Tylko administratorzy."""
    return {"message": "Panel administracyjny"}


@router.put("/content/{content_id}", dependencies=[Depends(require_roles("admin", "editor"))])
async def edit_content(content_id: int):
    """Administratorzy i edytorzy."""
    return {"message": f"Treść {content_id} zaktualizowana"}
