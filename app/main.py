"""Application entrypoint for the Notes CRUD API."""

from typing import Dict

from fastapi import FastAPI

from app.routes.note_routes import router as note_router

app = FastAPI(
    title="Notes CRUD API",
    description=(
        "A beginner-friendly FastAPI project demonstrating clean architecture, "
        "structured routing, and in-memory persistence."
    ),
    version="0.1.0",
)


@app.get("/health", tags=["Health"])
def health_check() -> Dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}


# Attach note routes under a versioned API prefix for clarity.
app.include_router(note_router, prefix="/api/v1")
