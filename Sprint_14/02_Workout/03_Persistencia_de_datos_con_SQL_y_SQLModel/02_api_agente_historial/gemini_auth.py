"""Carga GEMINI_API_KEY desde .env (obligatoria en la API)."""

import os
from pathlib import Path

from dotenv import load_dotenv

_configured = False
_ROOT = Path(__file__).resolve().parent


def configurar_gemini_api_key() -> None:
    """Lee `.env` en la raíz del workout. Sin key → error claro al arrancar."""
    global _configured
    if _configured:
        return

    load_dotenv(_ROOT / ".env")

    if not os.getenv("GEMINI_API_KEY"):
        raise RuntimeError(
            "Falta GEMINI_API_KEY. Copia .env.example → .env y pega tu key."
        )

    _configured = True
