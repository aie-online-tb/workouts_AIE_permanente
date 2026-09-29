# Guion — Multimodal: imagen → texto (con LangGraph)

**Material:** `02_multimodal_imagen_texto.ipynb`  
**Duración:** ~12–15 min

## Apertura

- Misma `GEMINI_API_KEY`; multimodal **dentro** de LangGraph (el proyecto final también usa grafo).
- Objetivo: cartel → nodo `leer_imagen` → `State.respuesta`.
- Diagrama: `START → leer_imagen → END`.

## Contenido

1. Setup: `langgraph` + `google-genai`.
2. Cargar `assets/cartel_demo.jpg` (mostrar en el notebook).
3. `EstadoVision` (`ruta_imagen`, `pregunta`, `respuesta`).
4. Nodo con `Part.from_bytes` + `Part.from_text`; grafo lineal + ASCII.
5. `invoke` y leer la respuesta del estado.

## Cierre

- Multimodal = parts; LangGraph = dónde vive el paso.
- En un agente mayor: mismo nodo/tool → el resto del grafo sigue con texto.
