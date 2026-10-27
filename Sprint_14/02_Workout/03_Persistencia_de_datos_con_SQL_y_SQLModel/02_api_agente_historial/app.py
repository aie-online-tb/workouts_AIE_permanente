"""
API FastAPI — agente cultural + historial SQLite (SQLModel).

  /ask → procesar_turno → save_turn (user + assistant)
  GET /threads/{id}/messages → listar historial

El checkpointer del grafo sigue en RAM; el historial de negocio va a historial.db.
Al reiniciar uvicorn, los mensajes SQL **siguen**.

Arranque:
  uvicorn app:app --reload --port 8000
  → http://127.0.0.1:8000/docs
"""

from contextlib import asynccontextmanager
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from gemini_auth import configurar_gemini_api_key
from schemas import ApproveIn, AskIn, AskOut, MessageOut
from src import db
from src.agent import aprobar_plan, procesar_turno
from src.state import crear_estado

configurar_gemini_api_key()

# Sesiones del agente en RAM (checkpointer / estado del grafo)
_sessions: Dict[str, dict] = {}
# Última pregunta por hilo (para guardar el turno tras /approve)
_last_pregunta: Dict[str, str] = {}


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Al arrancar: CREATE TABLE si historial.db aún no tiene schema
    db.ensure_schema()
    yield


app = FastAPI(
    title="API agente cultural + historial",
    description=(
        "Agente LangGraph por HTTP + historial SQLModel (SQLite). "
        "POST /ask guarda el turno; GET /threads/{id}/messages lo lista."
    ),
    lifespan=lifespan,
)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


def _estado_sesion(thread_id: str, pedido: str = "") -> dict:
    if thread_id not in _sessions:
        _sessions[thread_id] = crear_estado(pedido)
    return _sessions[thread_id]


def _a_ask_out(estado: dict, thread_id: str) -> AskOut:
    return AskOut(
        respuesta=estado.get("respuesta") or "",
        thread_id=thread_id,
        done=bool(estado.get("done", False)),
        pendiente_hitl=bool(estado.get("pendiente_hitl", False)),
        error=estado.get("error") or None,
    )


def _persistir_si_hay_respuesta(thread_id: str, pregunta: str, estado: dict) -> None:
    """Puente API → SQL: escribe user+assistant en historial.db vía db.save_turn."""
    respuesta = (estado.get("respuesta") or "").strip()
    if not respuesta:
        return
    db.save_turn(thread_id, pregunta, respuesta)


@app.get("/health")
def health():
    """Proceso vivo + motor de almacenamiento del historial."""
    return {"status": "ok", "storage": db.storage_mode()}


@app.post("/ask", response_model=AskOut)
def ask(body: AskIn) -> AskOut:
    """
    Un turno del agente. Tras responder, guarda user+assistant en SQLite.
    Con auto_aprobar=True, si hay HITL se aprueba y también se persiste.
    """
    pregunta = body.pregunta.strip()
    if not pregunta:
        raise HTTPException(status_code=400, detail="pregunta vacía")

    thread_id = (body.thread_id or "default").strip() or "default"
    estado = _estado_sesion(thread_id, pedido=pregunta)
    _last_pregunta[thread_id] = pregunta

    out = procesar_turno(estado, pregunta, thread_id)

    if body.auto_aprobar and out.get("pendiente_hitl"):
        out = aprobar_plan(thread_id, True, out)

    _sessions[thread_id] = out

    # Solo persistimos si el turno cerró (sin HITL pendiente)
    if not out.get("pendiente_hitl"):
        _persistir_si_hay_respuesta(thread_id, pregunta, out)

    return _a_ask_out(out, thread_id)


@app.post("/approve", response_model=AskOut)
def approve(body: ApproveIn) -> AskOut:
    """HITL manual; si hay respuesta, se guarda en el historial."""
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

    pregunta = _last_pregunta.get(thread_id, "")
    # Tras aprobar/rechazar, si ya no hay HITL, guardamos el turno en SQLite
    if pregunta and not out.get("pendiente_hitl"):
        _persistir_si_hay_respuesta(thread_id, pregunta, out)

    return _a_ask_out(out, thread_id)


@app.get("/threads/{thread_id}/messages", response_model=list[MessageOut])
def get_messages(thread_id: str) -> list[MessageOut]:
    """Lee el historial desde SQLite (no desde la RAM del agente)."""
    rows = db.list_messages(thread_id)
    return [MessageOut(**row) for row in rows]
