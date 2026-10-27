"""
Contratos HTTP de la API (Pydantic).
"""

from typing import Optional

from pydantic import BaseModel, Field


class AskIn(BaseModel):
    """Body de POST /ask — una pregunta al agente cultural."""

    pregunta: str = Field(..., min_length=1, max_length=2000)
    thread_id: Optional[str] = Field(default=None, max_length=100)
    auto_aprobar: bool = Field(
        default=True,
        description="Si hay plan pendiente HITL, aprobarlo automáticamente",
    )


class AskOut(BaseModel):
    """Respuesta de POST /ask y POST /approve."""

    respuesta: str
    thread_id: str
    done: bool = False
    pendiente_hitl: bool = False
    error: Optional[str] = None


class ApproveIn(BaseModel):
    """Body de POST /approve — HITL manual."""

    thread_id: str = Field(..., min_length=1, max_length=100)
    aprobado: bool = Field(..., description="True = aprobar plan; False = rechazar")


class MessageOut(BaseModel):
    """Un mensaje del historial SQL."""

    role: str
    content: str
    created_at: Optional[str] = None
