"""Tool: hora_actual."""

from datetime import datetime

from langchain_core.tools import tool


@tool
def hora_actual() -> str:
    """Devuelve la fecha y hora local actuales en formato ISO."""
    return datetime.now().isoformat(timespec="seconds")
