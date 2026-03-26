"""Domain model representing a Note entity."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Note:
    """Lightweight representation of a stored note."""

    id: int
    title: str
    content: str
    created_at: datetime
