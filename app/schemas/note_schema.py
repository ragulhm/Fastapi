"""Pydantic schemas for request validation and responses."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class NoteBase(BaseModel):
    """Shared attributes for incoming note payloads."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    content: Optional[str] = Field(default=None, min_length=1, max_length=1000)


class NoteCreate(NoteBase):
    """Payload schema for creating a new note."""

    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=1000)


class NoteUpdate(NoteBase):
    """Payload schema for partially updating an existing note."""

    @model_validator(mode="after")
    def ensure_some_value(cls, values: "NoteUpdate") -> "NoteUpdate":
        """Ensure that at least one field is provided when updating."""
        if values.title is None and values.content is None:
            raise ValueError("Provide at least one field to update.")
        return values


class NoteResponse(BaseModel):
    """Schema returned by the API for note resources."""

    id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
