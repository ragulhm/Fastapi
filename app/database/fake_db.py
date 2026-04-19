from datetime import datetime
from typing import List, Optional
from app.models.note import Note


class FakeNoteDB:
    """Simple in-memory repository that mimics database behavior."""

    def __init__(self) -> None:
        self._notes: List[Note] = []
        self._sequence: int = 1

    def list_notes(self) -> List[Note]:
        """Return a copy of stored notes."""
        return list(self._notes)

    def create_note(self, title: str, content: str) -> Note:
        """Persist a new note and return it."""
        note = Note(
            id=self._sequence,
            title=title,
            content=content,
            created_at=datetime.utcnow(),
        )
        self._sequence += 1
        self._notes.append(note)
        return note

    def get_note(self, note_id: int) -> Optional[Note]:
        """Retrieve a note by its identifier."""
        return next((note for note in self._notes if note.id == note_id), None)

    def update_note(
        self,
        note_id: int,
        *,
        title: Optional[str] = None,
        content: Optional[str] = None,
    ) -> Optional[Note]:
        """Update fields on a note if it exists."""
        note = self.get_note(note_id)
        if note is None:
            return None
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        return note

    def delete_note(self, note_id: int) -> bool:
        """Delete a note and return whether it existed."""
        note = self.get_note(note_id)
        if note is None:
            return False
        self._notes.remove(note)
        return True


fake_note_db = FakeNoteDB()
