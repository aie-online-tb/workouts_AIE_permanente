# Guion — Agente con tools en LangGraph (ReAct)

**Material:** `01_agente_tools_en_langgraph.ipynb`  
**Duración:** ~12–15 min

## Apertura

- Tras S12: el loop agentic ya lo conocéis; ahora el orquestador es un **grafo**.
- Frase clave: mismo contrato (LLM pide, Python ejecuta); cambia quién encadena los pasos.

## Contenido

1. Setup: `GEMINI_API_KEY` y `langchain-google-genai` (`gemini-2.5-flash`).
2. Esquema ReAct: `START → agent → router → tools → agent … → END`.
3. Tres `@tool`: `calcular`, `obtener_clima` (Open-Meteo + JSON fallback) y `buscar_dato`; `bind_tools`.
4. `EstadoAgente`: `add_messages` + contador `pasos` / `MAX_STEPS` (guardrail en Python).
5. `ToolNode`, router con `tool_calls`, `compile` y ASCII del grafo.
6. Ejecutar tres preguntas (math, clima, multi-tool).

## Cierre

- Tabla `@tool` / `ToolNode` / router / `MAX_STEPS`.
- Puente al proyecto: allowlist + `ejecutar_tool` de S12 dentro del nodo tools.
- Anunciar bloque 2: checkpoints y memoria.
