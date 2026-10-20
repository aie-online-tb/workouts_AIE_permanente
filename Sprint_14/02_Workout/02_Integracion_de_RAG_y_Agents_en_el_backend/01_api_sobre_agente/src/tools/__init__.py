"""Allowlist de tools LangChain (@tool).

Solo las tools de esta lista se pueden ejecutar.
Si el modelo pide otra, ejecutar_tool la bloquea.
"""

from src.tools.api_eventos import API_consultar_eventos_madrid
from src.tools.describir_cartel import describir_cartel
from src.tools.hora_actual import hora_actual
from src.tools.rag_guia import RAG_buscar_en_guia

TOOLS = [
    hora_actual,
    RAG_buscar_en_guia,
    API_consultar_eventos_madrid,
    describir_cartel,
]

TOOL_BY_NAME = {t.name: t for t in TOOLS}


def ejecutar_tool(nombre: str, args: dict | None = None) -> str:
    """Ejecuta una tool de la allowlist; si no está, bloquea."""
    args = args or {}
    tool = TOOL_BY_NAME.get(nombre)
    if tool is None:
        return f"Error: tool '{nombre}' no está permitida."
    try:
        return str(tool.invoke(args))
    except Exception as e:  # noqa: BLE001
        return f"Error: {e}"
