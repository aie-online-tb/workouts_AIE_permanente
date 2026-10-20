"""Tool: API_consultar_eventos_madrid — HTTP + fallback local."""

import json

import requests
from langchain_core.tools import tool

import config


@tool
def API_consultar_eventos_madrid(limite: int = 5) -> str:
    """Trae N eventos del catálogo cultural de Madrid. Si falla la red, usa fallback JSON."""
    try:
        limite = int(limite)
    except (TypeError, ValueError):
        limite = 5
    limite = max(1, min(limite, 10))

    try:
        resp = requests.get(
            config.MADRID_EVENTOS_URL,
            timeout=config.HTTP_TIMEOUT_SECONDS,
        )
        resp.raise_for_status()
        items = resp.json().get("@graph", [])
        fuente = "api"
    except Exception:
        data = json.loads(config.EVENTOS_FALLBACK_PATH.read_text(encoding="utf-8"))
        items = data.get("@graph", [])
        fuente = "fallback"

    if not items:
        return f"No hay eventos (fuente={fuente})."

    lineas = [f"Fuente: {fuente}", ""]
    for item in items[:limite]:
        titulo = item.get("title", "(sin título)")
        lugar = item.get("event-location", "?")
        fecha = item.get("dtstart", "?")
        lineas.append(f"- {titulo} | {lugar} | {fecha}")
    return "\n".join(lineas)
