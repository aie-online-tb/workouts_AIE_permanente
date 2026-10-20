"""Estado de producto (UI / CLI) y helpers.

crear_estado: plantilla que ven Streamlit / el JSON de la CLI.
estado_desde_grafo: copia al estado de producto los campos que salen del grafo.
"""

import copy
from typing import Any


def crear_estado(pedido: str = "") -> dict[str, Any]:
    """Plantilla visible en Streamlit / resumen CLI."""
    return {
        "objetivo": "Planificar una tarde cultural (multiagente LangGraph)",
        "pedido_original": pedido,
        "pedido": pedido,
        "notas_cultura": "",
        "notas_practico": "",
        "notas_vision": "",
        "respuesta": "",
        "plan": [],
        "siguiente": "",
        "iteracion": 0,
        "log": [],
        "traza_tools": [],
        "done": False,
        "error": None,
        "pendiente_hitl": False,
        "plan_aprobado": False,
        "preferencias": {
            "intereses": None,
            "presupuesto": None,
            "zona": None,
            "duracion_horas": None,
        },
        "traza": [],
    }


def estado_desde_grafo(resultado: dict[str, Any], base: dict[str, Any] | None = None) -> dict[str, Any]:
    """Fusiona la salida del grafo sobre el estado de producto (para la UI)."""
    nuevo = copy.deepcopy(base) if base else crear_estado()
    for clave in (
        "pedido",
        "notas_cultura",
        "notas_practico",
        "notas_vision",
        "respuesta",
        "plan",
        "siguiente",
        "iteracion",
        "log",
        "traza_tools",
        "done",
        "plan_aprobado",
        "pendiente_hitl",
    ):
        if clave in resultado:
            nuevo[clave] = resultado[clave]
    if resultado.get("pedido") and not nuevo.get("pedido_original"):
        nuevo["pedido_original"] = resultado["pedido"]
    return nuevo
