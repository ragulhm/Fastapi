"""Business logic for managing notes."""

from typing import List, Optional

from fastapi import HTTPException, status

from app.database.fake_db import FakeNoteDB, fake_note_db
from app.models.note import Note


class NoteService:
    """Encapsulates operations against the notes data store."""

    def __init__(self, database: FakeNoteDB = fake_note_db) -> None:
        self._database = database

    def create_note(self, *, title: str, content: str) -> Note:
        """Create and persist a new note."""
        return self._database.create_note(title=title, content=content)

    def list_notes(self, limit: int) -> List[Note]:
        """Return a bounded list of notes."""
        return self._database.list_notes()[:limit]

    def get_note(self, note_id: int) -> Note:
        """Fetch a single note or raise a 404 error."""
        note = self._database.get_note(note_id)
        if note is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note with id {note_id} not found.",
            )
        return note

    def update_note(
        self,
        note_id: int,
        *,
        title: Optional[str],
        content: Optional[str],
    ) -> Note:
        """Update an existing note and return it."""
        note = self._database.update_note(note_id, title=title, content=content)
        if note is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note with id {note_id} not found.",
            )
        return note

    def delete_note(self, note_id: int) -> None:
        """Delete a note, raising if it does not exist."""
        deleted = self._database.delete_note(note_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note with id {note_id} not found.",
            )
