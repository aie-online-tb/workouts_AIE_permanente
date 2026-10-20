"""Modelos SQLModel del historial.

Cada clase con table=True = una tabla en historial.db.
Relación 1–N: una Conversation tiene muchos Message (FK thread_id).
"""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


def _now() -> datetime:
    """Marca de tiempo en UTC al crear la fila."""
    return datetime.now(timezone.utc)


class Conversation(SQLModel, table=True):
    """Un hilo de chat (= el thread_id que manda el cliente en /ask)."""

    # PK string: usamos el mismo id que la API (p. ej. "demo-db")
    id: str = Field(primary_key=True, max_length=100)
    created_at: datetime = Field(default_factory=_now)


class Message(SQLModel, table=True):
    """Un mensaje dentro de un hilo (pregunta o respuesta)."""

    # PK autoincremental: SQLite asigna el id al hacer commit (default=None)
    id: Optional[int] = Field(default=None, primary_key=True)
    # FK → conversation.id (une Message con su Conversation en SQL)
    thread_id: str = Field(foreign_key="conversation.id", index=True, max_length=100)
    role: str = Field(max_length=20)  # "user" | "assistant"
    content: str
    created_at: datetime = Field(default_factory=_now)
