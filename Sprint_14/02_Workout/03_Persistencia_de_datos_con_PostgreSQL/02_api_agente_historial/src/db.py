"""Persistencia del historial con SQLModel + SQLite.

Este módulo es lo que la API llama para escribir/leer historial.db.
Modelos → src/models.py | Quién llama → app.py (tras /ask o /approve).
"""

from typing import Any

from sqlmodel import Session, SQLModel, create_engine, select

import config
from src.models import Conversation, Message

# Conexión al fichero SQLite (historial.db). Sin servidor.
engine = create_engine(config.DATABASE_URL, echo=False)


def ensure_schema() -> None:
    """Crea las tablas si no existen (se llama al arrancar FastAPI)."""
    # CREATE TABLE según Conversation / Message (si ya están, no hace nada)
    SQLModel.metadata.create_all(engine)


def save_turn(thread_id: str, pregunta: str, respuesta: str) -> None:
    """Guarda un turno completo: mensaje user + mensaje assistant."""
    # Session = unidad de trabajo con la DB (abrir → cambios → commit)
    with Session(engine) as session:
        # Si el hilo no existe aún, creamos la Conversation
        if session.get(Conversation, thread_id) is None:
            session.add(Conversation(id=thread_id))
            session.commit()

        # Dos filas en message (pregunta + respuesta)
        session.add(Message(thread_id=thread_id, role="user", content=pregunta))
        session.add(
            Message(thread_id=thread_id, role="assistant", content=respuesta)
        )
        # Sin commit, los add solo están en memoria
        session.commit()


def list_messages(thread_id: str) -> list[dict[str, Any]]:
    """Lista mensajes del hilo ordenados por id (para GET …/messages)."""
    with Session(engine) as session:
        rows = session.exec(
            select(Message)
            .where(Message.thread_id == thread_id)
            .order_by(Message.id)
        ).all()
    # Devolvemos dicts simples (no objetos SQLModel) para el schema MessageOut
    return [
        {
            "role": m.role,
            "content": m.content,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }
        for m in rows
    ]


def storage_mode() -> str:
    """Valor que muestra /health → "storage": "sqlite"."""
    return "sqlite"
