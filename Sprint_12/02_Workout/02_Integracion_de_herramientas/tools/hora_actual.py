"""Tool: hora_actual."""

from datetime import datetime


def hora_actual() -> str:
    """Devuelve la fecha y hora local actuales en formato ISO."""
    return datetime.now().isoformat(timespec="seconds")
