"""Orquestación: procesar_turno + HITL (interrupt_before aplicar)."""

import logging
import uuid
from typing import Any

import config
from src.graph import (
    config_hilo,
    estado_inicial_grafo,
    get_app,
    hay_interrupt,
)
from src.state import crear_estado, estado_desde_grafo

logger = logging.getLogger("uvicorn.error")


def _marcar_hitl(estado: dict[str, Any], thread_id: str) -> dict[str, Any]:
    """Si el grafo está pausado ante aplicar, marca pendiente_hitl para la UI."""
    pendiente = hay_interrupt(thread_id)
    estado = dict(estado)
    estado["pendiente_hitl"] = pendiente
    if pendiente:
        estado["done"] = False
        resp = (estado.get("respuesta") or "").rstrip()
        aviso = "\n\n_(Plan listo: aprueba o rechaza antes de cerrar.)_"
        if "aprueba o rechaza" not in resp.lower():
            estado["respuesta"] = resp + aviso
    return estado


def procesar_turno(
    estado: dict[str, Any],
    mensaje: str,
    thread_id: str,
    max_steps: int | None = None,
) -> dict[str, Any]:
    """Un mensaje de usuario → un invoke del grafo multiagente.

    Puede terminar en pausa HITL (antes de aplicar). El mismo thread_id
    reutiliza el checkpointer MemorySaver.
    """
    mensaje = (mensaje or "").strip()
    if not mensaje:
        nuevo = dict(estado)
        nuevo["respuesta"] = "Escribe un mensaje (intereses, presupuesto, zona…)."
        return nuevo

    app = get_app()
    cfg = config_hilo(thread_id)
    n = len(estado.get("traza") or []) + 1

    try:
        inicial = estado_inicial_grafo(mensaje, max_steps=max_steps)
        resultado = app.invoke(inicial, cfg)
        nuevo = estado_desde_grafo(resultado, estado)
        nuevo["error"] = None
        if not nuevo.get("pedido_original"):
            nuevo["pedido_original"] = mensaje
        nuevo = _marcar_hitl(nuevo, thread_id)
        nuevo.setdefault("traza", []).append(
            {
                "turno": n,
                "mensaje": mensaje,
                "status": "ok",
                "done": nuevo.get("done"),
                "pendiente_hitl": nuevo.get("pendiente_hitl"),
                "log": list(resultado.get("log") or []),
                "tools": list(resultado.get("traza_tools") or []),
            }
        )
        return nuevo
    except Exception as e:  # noqa: BLE001
        logger.exception("Fallo en procesar_turno (thread_id=%s)", thread_id)
        nuevo = dict(estado)
        nuevo["error"] = str(e)
        nuevo["respuesta"] = (
            "No he podido continuar por un error técnico. "
            "Revisa la API key o la respuesta del modelo."
        )
        nuevo.setdefault("traza", []).append(
            {
                "turno": n,
                "mensaje": mensaje,
                "status": "error",
                "detail": str(e),
                "tools": [],
            }
        )
        return nuevo


def aprobar_plan(thread_id: str, aprobado: bool, estado: dict[str, Any]) -> dict[str, Any]:
    """HITL: guarda la decisión en el checkpoint y reanuda el nodo aplicar.

    1) update_state(plan_aprobado=...)
    2) invoke(None) → continúa desde interrupt_before sin input nuevo
    """
    app = get_app()
    cfg = config_hilo(thread_id)
    if not hay_interrupt(thread_id):
        nuevo = dict(estado)
        nuevo["respuesta"] = "No hay plan pendiente de aprobación."
        return nuevo

    app.update_state(cfg, {"plan_aprobado": bool(aprobado)})
    resultado = app.invoke(None, cfg)
    nuevo = estado_desde_grafo(resultado, estado)
    nuevo["error"] = None
    nuevo["pendiente_hitl"] = False
    nuevo.setdefault("traza", []).append(
        {
            "turno": len(estado.get("traza") or []) + 1,
            "mensaje": "HITL:" + ("aprobar" if aprobado else "rechazar"),
            "status": "ok",
            "done": nuevo.get("done"),
            "pendiente_hitl": False,
            "tools": [],
        }
    )
    return nuevo


def nuevo_thread_id() -> str:
    return f"cultural-{uuid.uuid4().hex[:8]}"


def run_demo(
    mensajes: list[str] | None = None,
    max_turns: int | None = None,
    max_steps: int | None = None,
    auto_aprobar: bool = True,
    thread_id: str | None = None,
) -> dict[str, Any]:
    """Demo CLI: pedido(s) → posible HITL (auto-aprobado si auto_aprobar=True)."""
    msgs = list(mensajes) if mensajes is not None else list(config.DEMO_MENSAJES)
    limit = max_turns if max_turns is not None else config.MAX_TURNS_DEFAULT
    tid = thread_id or nuevo_thread_id()
    estado = crear_estado(msgs[0] if msgs else "")

    for mensaje in msgs[:limit]:
        if estado.get("done") or estado.get("error"):
            break
        estado = procesar_turno(estado, mensaje, tid, max_steps=max_steps)
        if estado.get("pendiente_hitl") and auto_aprobar:
            estado = aprobar_plan(tid, True, estado)

    estado["thread_id"] = tid
    return estado
