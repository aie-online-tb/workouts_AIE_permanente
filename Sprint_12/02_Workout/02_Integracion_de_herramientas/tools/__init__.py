"""El fichero __init__.py hace que `tools/` sea un paquete. Puedes hacer
`from tools import ejecutar_tool` además de importar cada módulo.

Aquí vive la allowlist: solo las tools de TOOL_REGISTRY se pueden ejecutar.
"""

from tools.api_eventos import API_consultar_eventos_madrid
from tools.hora_actual import hora_actual
from tools.rag_guia import RAG_buscar_en_guia

# Solo estas tools se pueden ejecutar (allowlist).
TOOL_REGISTRY = {
    "hora_actual": hora_actual,
    "RAG_buscar_en_guia": RAG_buscar_en_guia,
    "API_consultar_eventos_madrid": API_consultar_eventos_madrid,
}


def validar_args(nombre, args=None):
    """Guardrails: valida los args de las tools y pone un tope a
    cuántos eventos pide la API. En el futuro profundizaremos en esto."""
    args = args or {}
    if nombre == "hora_actual":
        return {}
    if nombre == "RAG_buscar_en_guia":
        return {"consulta": str(args.get("consulta") or "").strip()}
    if nombre == "API_consultar_eventos_madrid":
        try:
            limite = int(args.get("limite", 5))
        except (TypeError, ValueError):
            limite = 5
        return {"limite": max(1, min(limite, 10))}
    return args


def ejecutar_tool(nombre, args=None):
    """Si el nombre no está en el registro, no se ejecuta."""
    if nombre not in TOOL_REGISTRY:
        return f"Error: tool '{nombre}' no está permitida."
    limpios = validar_args(nombre, args)
    try:
        return TOOL_REGISTRY[nombre](**limpios)
    except Exception as e:
        return f"Error al ejecutar {nombre}: {e}"
