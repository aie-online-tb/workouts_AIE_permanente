# Guion — Proyecto agente LangGraph · tarde cultural

**Material:** [`05_proyecto_agente_langgraph_tarde_cultural/`](../../01_Teoria/03_Multimodal_multiagente_y_cierre/05_proyecto_agente_langgraph_tarde_cultural/) (teoría)  
**Duración:** ~12–15 min

## Apertura

- Cierre del sprint: juntáis ReAct, checkpoints, HITL y el dominio de S11/S12.
- Código completo en teoría; el workout apunta con [`02_proyecto_agente_langgraph_tarde_cultural.md`](../02_proyecto_agente_langgraph_tarde_cultural.md).

## Contenido

1. Estructura: `src/graph.py` (agent ↔ tools), `agent.py`, tools con allowlist, `app.py` Streamlit.
2. `MemorySaver` + `thread_id` compartido entre CLI y UI.
3. Pausa HITL cuando el plan está listo y falta aprobación humana.
4. Demo: `python main.py` y `streamlit run app.py` — plan borrador, Aprobar/Rechazar.
5. Contrato heredado: `procesar_turno`, `done` calculado en Python, traza de tools.
6. (Opcional) fallback JSON si falla la API de eventos.

## Cierre

- Este proyecto sustituye el `while` de S12 por LangGraph en producción pedagógica.
- Live Review / práctica evaluable alineada con el mismo patrón.
- Recordatorio: multiagente del bloque 3 es panorama, no requisito del proyecto.
