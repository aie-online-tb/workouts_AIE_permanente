# Guion — Carga de documentos y chunking

**Material:** `01_carga_documentos_y_chunking.ipynb`

**Duración aproximada:** ~20 min

**Datos:** un solo tema — agenda cultural Madrid (faq + guía + pdf + csv).

---

## Apertura (~30 s)

- Tres formas de cargar: **.md/.txt**, **.pdf**, **csv→Document**.
- Un solo open data: agenda de [datos.madrid.es](https://datos.madrid.es).

## Setup (~1 min)

- `%pip install` si hace falta.
- Muestra los 4 archivos en `data/` (faq, guía, pdf agenda, csv agenda).

## §1 TextLoader — FAQ y guía (~3 min)

- Carga `faq_agenda_cultural.md` y `guia_agenda_cultural.txt`.
- Mismo tema que el CSV; distinto formato (.md / .txt).

## §2 PyPDFLoader — documentación agenda (~3 min)

- `206974-3-agenda-eventos-culturales-100.pdf`.
- Un Document por página; metadata con `page`.

## §3 CSV → Document — eventos (~5 min)

- Mismo dataset en tabular; **1 fila = 1 `Document` construido a mano**.
- Frase clave en cámara: *TextLoader/PyPDFLoader ya devuelven Document; en CSV no hay loader útil — lo creamos nosotros*.
- Encoding `latin-1`; metadatos `id_evento`, `distrito`, `tipo`.
- Enlace al patrón que verán en `load.py` del proyecto (`cargar_agenda_csv`).

## §4 Unir fuentes (~1 min)

- Suma texto + pdf + eventos; imprime conteos.

## §5 Limpieza (~2 min)

- `normalizar_texto` → *vive en `clean.py` en el proyecto*.

## §6 Chunking (~3 min)

- 800/100; documentos vs chunks.

## §7 Experimento chunk_size (~2 min)

- 400 / 800 / 1500.

## §8 Inspección (~2 min)

- Chunk FAQ vs chunk cine gratuito del CSV.
- *¿Mezclan fuentes o cada uno sirve para su pregunta?*

## Cierre (~30 s)

- json/xml/rdf: mismo dataset, no hoy.
- Bloque 3: proyecto modular en `03_Embeddings/03_proyecto_rag_ingesta_chunking_embeddings.md`.
