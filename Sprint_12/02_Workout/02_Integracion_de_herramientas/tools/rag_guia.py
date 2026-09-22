"""Tool: RAG_buscar_en_guia — búsqueda en guía local (retrieve mínimo).

Qué hace esta tool (sí implementado):
  1. Cargar el fichero de la guía
  2. Partirlo en trozos (secciones ##)
  3. Recuperar los trozos más parecidos a la consulta (por palabras)
  4. Devolver ese texto como string

Qué NO hace (queda fuera a propósito):
  - Embeddings / vectores
  - Base vectorial (Chroma, FAISS…)
  - Indexado previo
  - Generar la respuesta final al usuario (eso lo hace el modelo
    después de recibir el resultado de la tool)

En un RAG “completo”: load → chunk → embed → index → retrieve → generate.
Aquí solo: load → chunk → retrieve (léxico).
"""

import re

import config


def _tokens(texto: str) -> set[str]:
    return {t for t in re.findall(r"\w+", texto.lower()) if len(t) > 2}


def _chunkear(texto: str) -> list[str]:
    """Parte la guía por secciones ##."""
    partes = re.split(r"\n(?=##\s)", texto.strip())
    chunks = [p.strip() for p in partes if p.strip()]
    return chunks or [texto.strip()]


def RAG_buscar_en_guia(consulta: str) -> str:
    """Busca en la guía cultural y devuelve pasajes relevantes (top-k)."""
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
