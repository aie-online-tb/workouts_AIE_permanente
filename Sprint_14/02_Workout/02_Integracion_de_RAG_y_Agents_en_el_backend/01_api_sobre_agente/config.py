"""Configuración — paths, modelo y defaults del agente cultural."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"

GEMINI_MODEL = "gemini-3.1-flash-lite-preview"
TEMPERATURE = 0.3
MAX_STEPS_DEFAULT = 4
MAX_TURNS_DEFAULT = 6
MAX_ITER = 8

MADRID_EVENTOS_URL = (
    "https://datos.madrid.es/egob/catalogo/206974-0-agenda-eventos-culturales-100.json"
)
HTTP_TIMEOUT_SECONDS = 12

GUIA_PATH = DATA_DIR / "guia_cultural.txt"
EVENTOS_FALLBACK_PATH = DATA_DIR / "eventos_fallback.json"

# Cartel multimodal: preferir assets/ local; si falta, otra copia del material del bootcamp
_CARTEL_LOCAL = ASSETS_DIR / "cartel_demo.jpg"
_CARTEL_FALLBACK = (
    ROOT.parents[4]
    / "06_AI_Agents_Engineering"
    / "Sprint_13"
    / "01_Teoria"
    / "03_Multimodal_multiagente_y_cierre"
    / "04_proyecto_agente_langgraph_tarde_cultural"
    / "assets"
    / "cartel_demo.jpg"
)
CARTEL_DEFAULT_PATH = (
    _CARTEL_LOCAL if _CARTEL_LOCAL.exists() else _CARTEL_FALLBACK
)

DEMO_MENSAJES = [
    (
        "Quiero una tarde cultural barata en el centro de Madrid: "
        "museo o exposición y algo de música si encaja. "
        "Consulta la guía y el catálogo de eventos."
    ),
]
