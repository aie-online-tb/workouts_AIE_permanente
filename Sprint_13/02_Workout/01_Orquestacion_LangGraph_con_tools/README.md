![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Orquestación LangGraph con tools (Sprint 13)

Primer bloque de workout del sprint: pasáis del `while` de S12 al **grafo ReAct** (`agent` ↔ `tools`).

Dominio de demo: `calcular` y `buscar_dato` locales; `obtener_clima` vía **Open-Meteo** con fallback en [`data/clima_fallback.json`](./data/clima_fallback.json).

| Notebook | Qué aprendéis |
|----------|----------------|
| [`01_agente_tools_en_langgraph.ipynb`](./01_agente_tools_en_langgraph.ipynb) | `@tool`, `ToolNode`, router ReAct y `MAX_STEPS` en Python |

Teoría: [`01_Teoria/01_Orquestacion_LangGraph_con_tools/`](../../01_Teoria/01_Orquestacion_LangGraph_con_tools/)

Prerrequisito: S12 — [`04_LangGraph_basico`](../../../Sprint_12/02_Workout/04_LangGraph_basico/)

## Dependencias

En la primera celda de cada notebook:

```bash
# %pip install -qU langgraph langchain-google-genai langchain-core python-dotenv requests
```
