from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.auth.auth0 import CurrentUser
from app.auth.permissions import ReadDocuments, WriteDocuments

router = APIRouter(prefix="/documents", tags=["documents"])


class DocumentCreate(BaseModel):
    title: str
    content: str


@router.get("/")
async def list_documents(user: ReadDocuments):
    """Wymaga uprawnienia 'read:documents'."""
    return {
        "user_id": user.sub,
        "documents": [
            {"id": 1, "title": "Regulamin"},
            {"id": 2, "title": "Polityka prywatności"},
        ],
    }


@router.post("/")
async def create_document(data: DocumentCreate, user: WriteDocuments):
    """Wymaga uprawnienia 'write:documents'."""
    return {"message": "Dokument utworzony", "title": data.title}


@router.delete("/{document_id}")
async def delete_document(document_id: int, current_user: CurrentUser):
    """Ręczne sprawdzenie permissions (alternatywa do gotowych typów)."""
    if "delete:documents" not in current_user.permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Brak uprawnienia 'delete:documents'",
        )
    return {"message": f"Dokument {document_id} usunięty"}
