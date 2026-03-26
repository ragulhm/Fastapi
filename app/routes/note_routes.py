"""API routes for managing notes."""

from typing import List

from fastapi import APIRouter, Query, status

from app.schemas.note_schema import NoteCreate, NoteResponse, NoteUpdate
from app.services.note_service import NoteService

router = APIRouter(tags=["Notes"])
service = NoteService()


@router.get(
    "/notes",
    response_model=List[NoteResponse],
    status_code=status.HTTP_200_OK,
)
def list_notes(limit: int = Query(default=10, ge=1, le=100, description="Maximum notes to return")):
    """Return a paginated collection of notes."""
    return service.list_notes(limit)


@router.get(
    "/notes/{note_id}",
    response_model=NoteResponse,
    status_code=status.HTTP_200_OK,
)
def get_note(note_id: int):
    """Return a single note by identifier."""
    return service.get_note(note_id)


@router.post(
    "/notes",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_note(payload: NoteCreate):
    """Create a new note resource."""
    return service.create_note(title=payload.title, content=payload.content)


@router.put(
    "/notes/{note_id}",
    response_model=NoteResponse,
    status_code=status.HTTP_200_OK,
)
def update_note(note_id: int, payload: NoteUpdate):
    """Update attributes on an existing note."""
    return service.update_note(
        note_id,
        title=payload.title,
        content=payload.content,
    )


@router.delete(
    "/notes/{note_id}",
    status_code=status.HTTP_200_OK,
)
def delete_note(note_id: int):
    """Delete a note and confirm removal."""
    service.delete_note(note_id)
    return {"message": f"Note {note_id} deleted."}
