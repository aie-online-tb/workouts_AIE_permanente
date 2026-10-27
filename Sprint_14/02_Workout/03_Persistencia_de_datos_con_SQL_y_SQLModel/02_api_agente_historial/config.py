"""Configuración — agente cultural + SQLite para el historial."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"

# URL del motor SQLModel: fichero local historial.db (sin servidor Postgres).
DATABASE_URL = f"sqlite:///{ROOT / 'historial.db'}"

GEMINI_MODEL = "gemini-3.1-flash-lite-preview"
TEMPERATURE = 0.3
MAX_STEPS_DEFAULT = 2
MAX_TURNS_DEFAULT = 6
MAX_ITER = 3

MADRID_EVENTOS_URL = (
    "https://datos.madrid.es/egob/catalogo/206974-0-agenda-eventos-culturales-100.json"
)
HTTP_TIMEOUT_SECONDS = 12

GUIA_PATH = DATA_DIR / "guia_cultural.txt"
EVENTOS_FALLBACK_PATH = DATA_DIR / "eventos_fallback.json"

# Cartel de demo (en assets/ de este proyecto)
CARTEL_DEFAULT_PATH = ASSETS_DIR / "cartel_demo.jpg"

DEMO_MENSAJES = [
    (
        "Quiero una tarde cultural barata en el centro de Madrid: "
        "museo o exposición y algo de música si encaja. "
        "Consulta la guía y el catálogo de eventos."
    ),
]
