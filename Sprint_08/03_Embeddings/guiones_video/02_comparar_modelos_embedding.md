# Guion — Comparar modelos de embedding

**Material:** `02_comparar_modelos_embedding.ipynb`

**Duración aproximada:** ~20 min

**Prerrequisito:** [`01_embeddings.ipynb`](../01_embeddings.ipynb) (API Gemini) y coseno en teoría.

---

## Apertura (~1 min)

- Objetivo: **comparar proveedores** con 3 frases fijas (P1, P2 programación; G1 gastronomía).
- Métricas: dimensiones, latencia, sim_parecido, sim_distinto, **contraste**.
- No mezclar espacios vectoriales entre proveedores.

## Setup y minidataset (~2 min)

- Tabla P1 / P2 / G1 en pantalla.
- Explicar contraste = sim(P1,P2) − sim(P1,G1).

## Gemini (~4 min)

- `types.Content` por frase (mismo patrón que `01_embeddings.ipynb`).
- Preview dims + línea de métricas.

## Hugging Face nube (~4 min)

- Primera vez con HF en el bootcamp: Inference API, 384 dims.
- Mismas métricas; comparar contraste con Gemini.

## Cohere (~3 min)

- Tercer proveedor en nube; 1024 dims.
- Latencia suele ser competitiva.

## HF local (opcional, ~2 min)

- `sentence-transformers` en CPU; descarga del modelo la primera vez.
- Mismas métricas de contraste que HF nube si es el mismo modelo.

## Tabla y gráficos (~3 min)

- Tabla ordenada por contraste.
- Barras P1–P2 vs P1–G1; PCA 2D por proveedor (subplots separados).

## Cierre (~1 min)

- Recomendación del módulo: **Gemini** (`gemini-embedding-2`) para coherencia con `01_embeddings.ipynb` y el proyecto — aunque otro modelo gane en este minidataset.
- Siguiente: [`03_proyecto_rag_ingesta_chunking_embeddings.md`](../03_proyecto_rag_ingesta_chunking_embeddings.md) — pipeline completo con el corpus real (repositorio en GitHub).
