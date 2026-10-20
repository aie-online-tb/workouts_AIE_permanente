"""
API FastAPI sobre el agente cultural (LangGraph).

El agente (procesar_turno / aprobar_plan) se da por hecho.
Esta demo centra en la capa HTTP:

  cliente (/docs) → FastAPI → procesar_turno / aprobar_plan → grafo + tools

El estado de producto vive en un dict en RAM, indexado por thread_id.
Al reiniciar uvicorn se pierde.

Arranque:
  uvicorn app:app --reload --port 8000
  → http://127.0.0.1:8000/docs
"""

from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from gemini_auth import configurar_gemini_api_key
from schemas import ApproveIn, AskIn, AskOut
from src.agent import aprobar_plan, procesar_turno
from src.state import crear_estado

# Carga GEMINI_API_KEY desde .env (obligatoria para el agente)
configurar_gemini_api_key()

app = FastAPI(
    title="API sobre agente cultural",
    description=(
        "API HTTP sobre un agente multiagente cultural (LangGraph). "
        "POST /ask → procesar_turno; POST /approve → HITL."
    ),
)

# Sesiones en memoria: thread_id → estado de producto
_sessions: Dict[str, dict] = {}


@app.get("/", include_in_schema=False)
def root():
    """La raíz no tiene página: el cliente de esta demo es Swagger."""
    return RedirectResponse(url="/docs")


def _estado_sesion(thread_id: str, pedido: str = "") -> dict:
    """Devuelve el estado del hilo o crea uno nuevo."""
    if thread_id not in _sessions:
        _sessions[thread_id] = crear_estado(pedido)
    return _sessions[thread_id]


def _a_ask_out(estado: dict, thread_id: str) -> AskOut:
    """Traduce el dict del agente al contrato HTTP AskOut."""
    return AskOut(
        respuesta=estado.get("respuesta") or "",
        thread_id=thread_id,
        done=bool(estado.get("done", False)),
        pendiente_hitl=bool(estado.get("pendiente_hitl", False)),
        error=estado.get("error") or None,
    )


@app.get("/health")
def health():
    """¿Proceso vivo? No llama al LLM."""
    return {"status": "ok"}


@app.post("/ask", response_model=AskOut)
def ask(body: AskIn) -> AskOut:
    """
    Un turno del agente cultural.
    `auto_aprobar=True` (default): si queda pendiente HITL, aprueba solo
    (útil en Swagger). Con `auto_aprobar=False` usad POST /approve.
    """
    pregunta = body.pregunta.strip()
    if not pregunta:
        raise HTTPException(status_code=400, detail="pregunta vacía")

    thread_id = (body.thread_id or "default").strip() or "default"
    estado = _estado_sesion(thread_id, pedido=pregunta)

    # Firma del agente: (estado, mensaje, thread_id)
    out = procesar_turno(estado, pregunta, thread_id)

    # Modo demo cómodo: cerrar el HITL sin segundo request
    if body.auto_aprobar and out.get("pendiente_hitl"):
        out = aprobar_plan(thread_id, True, out)

    _sessions[thread_id] = out
    return _a_ask_out(out, thread_id)


@app.post("/approve", response_model=AskOut)
def approve(body: ApproveIn) -> AskOut:
    """HITL manual: aprobar o rechazar el plan pendiente de un thread_id."""
    thread_id = body.thread_id.strip()
    if thread_id not in _sessions:
        raise HTTPException(
            status_code=404,
            detail="No hay sesión para ese thread_id. Haz antes un POST /ask.",
        )

    estado = _sessions[thread_id]
    if not estado.get("pendiente_hitl"):
        raise HTTPException(
            status_code=400,
            detail="No hay plan pendiente de aprobación en este hilo.",
        )

    out = aprobar_plan(thread_id, body.aprobado, estado)
    _sessions[thread_id] = out
    return _a_ask_out(out, thread_id)
