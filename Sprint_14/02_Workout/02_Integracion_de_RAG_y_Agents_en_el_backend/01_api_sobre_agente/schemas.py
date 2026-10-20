"""
Contratos HTTP de la API (Pydantic).

FastAPI usa estas clases para validar el JSON de entrada/salida
y generar la documentación de /docs (Swagger).
"""

from typing import Optional

from pydantic import BaseModel, Field


class AskIn(BaseModel):
    """Body de POST /ask — una pregunta al agente cultural."""

    pregunta: str = Field(..., min_length=1, max_length=2000)
    # Optional[str] = hilo opcional; si no viene, la API usa "default"
    thread_id: Optional[str] = Field(default=None, max_length=100)
    # Si True y el grafo queda en HITL, la API auto-aprueba el plan (cómodo en Swagger)
    auto_aprobar: bool = Field(
        default=True,
        description="Si hay plan pendiente HITL, aprobarlo automáticamente",
    )


class AskOut(BaseModel):
    """Respuesta de POST /ask y POST /approve."""

    respuesta: str
    thread_id: str
    done: bool = False
    # True = el grafo espera aprobación humana (usar POST /approve)
    pendiente_hitl: bool = False
    # Mensaje de la excepción si el turno falló; null si no hubo error
    error: Optional[str] = None


class ApproveIn(BaseModel):
    """Body de POST /approve — HITL manual."""

    thread_id: str = Field(..., min_length=1, max_length=100)
    aprobado: bool = Field(..., description="True = aprobar plan; False = rechazar")
