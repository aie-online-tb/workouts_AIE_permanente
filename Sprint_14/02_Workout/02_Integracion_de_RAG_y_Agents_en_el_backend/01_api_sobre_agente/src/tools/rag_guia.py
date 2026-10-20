"""Tool: RAG_buscar_en_guia — mini-RAG léxico (S12) sobre la guía cultural."""

import re

from langchain_core.tools import tool

import config


def _tokens(texto: str) -> set[str]:
    return {t for t in re.findall(r"\w+", texto.lower()) if len(t) > 2}


def _chunkear(texto: str) -> list[str]:
    partes = re.split(r"\n(?=##\s)", texto.strip())
    chunks = [p.strip() for p in partes if p.strip()]
    return chunks or [texto.strip()]


@tool
def RAG_buscar_en_guia(consulta: str) -> str:
    """Busca en la guía cultural local y devuelve pasajes relevantes (top-k)."""
    consulta = (consulta or "").strip()
    if not consulta:
        return "Error: consulta vacía."

    path = config.GUIA_PATH
    if not path.exists():
        return f"Error: no encuentro la guía en {path}"

    try:
        texto = path.read_text(encoding="utf-8")
    except OSError as e:
        return f"Error al leer la guía: {e}"

    chunks = _chunkear(texto)
    q = _tokens(consulta)
    ranked = sorted(chunks, key=lambda c: len(q & _tokens(c)), reverse=True)
    top = [c for c in ranked[:2] if len(q & _tokens(c)) > 0]
    if not top:
        return f"No encontré nada en la guía sobre: {consulta}"
    return "\n\n---\n\n".join(top)
