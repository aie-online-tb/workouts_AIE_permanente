# Guion — Embeddings con Gemini

**Material:** `01_embeddings.ipynb`

**Duración aproximada:** ~15 min

**Prerrequisito:** teoría [Vectores y similitud semántica](../../../01_Teoria/03_Embeddings/01_vectores_y_similitud_semantica.md) (coseno).

---

## Apertura (~45 s)

- Un **embedding** convierte texto en una lista de números (vector). Textos parecidos → vectores cercanos.
- En RAG: embeddeas chunks **y** la pregunta del usuario con el **mismo modelo**; luego buscas el chunk más cercano (Sprint 9: ChromaDB).
- Modelo del notebook: **`gemini-embedding-2`** (3072 dimensiones por defecto).

## Dependencias y setup (~2 min)

- `%pip install google-genai python-dotenv` si hace falta.
- `load_dotenv()` + **`getpass`** si no hay `GEMINI_API_KEY` en `.env` — no mostrar la clave al pegarla.
- Imprime `Cliente OK, modelo: gemini-embedding-2`.

## §1 — Embeddear una frase (~4 min)

- Pregunta de demo: *«¿Hay eventos culturales gratuitos en Madrid este verano?»*
- `client.models.embed_content` → `result.embeddings[0].values`.
- Mostrar **3072** dimensiones y los primeros floats (no interpretar cada número).

## §2 — Embeddear varios chunks (~7 min)

- Tres chunks **inline** (mismo formato que `chunks.json` del proyecto):
  - FAQ agenda (`faq_agenda_cultural.md`)
  - Evento cine gratuito del CSV (Hortaleza)
  - Guía tipos de actividad (`guia_agenda_cultural.txt`)
- Inspeccionar `metadata` de cada chunk antes de embeddear.

### Trampa didáctica — `types.Content` (~3 min dentro de §2)

- Con `gemini-embedding-2`, `contents=["a", "b", "c"]` puede devolver **un solo** embedding agregado.
- Solución: **un `types.Content` por texto** → `Embeddings recibidos: 3 (esperados: 3)` y tres líneas con **3072 dims** cada una.
- Frase en cámara: *«Un vector por chunk; si no, el RAG no puede elegir el fragmento correcto.»*

## Puente al siguiente notebook (~1 min)

- Aquí **no** comparamos pregunta vs chunks (eso es retrieval).
- Siguiente workout: [`02_comparar_modelos_embedding.ipynb`](../02_comparar_modelos_embedding.ipynb) — medir si un modelo separa bien los temas.
- Proyecto del módulo: `python main.py` → `chunks.json` + `embeddings.json` (mismo patrón API en `embed.py`).

## Cierre (~30 s)

- Regla de oro: **un solo modelo** de embedding en todo el pipeline.
- Sprint 9: indexar en ChromaDB y recuperar por similitud.
