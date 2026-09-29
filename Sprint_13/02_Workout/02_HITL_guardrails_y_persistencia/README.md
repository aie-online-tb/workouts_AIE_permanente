![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# HITL, guardrails y persistencia (Sprint 13)

Segundo bloque: **memoria entre turnos** y **human-in-the-loop** antes de aplicar un plan.

Estos patrones los enlazaréis con Streamlit en el proyecto cultural (`thread_id`, botones Aprobar/Rechazar).

| Notebook | Qué aprendéis |
|----------|----------------|
| [`01_memoria_y_checkpoints.ipynb`](./01_memoria_y_checkpoints.ipynb) | `MemorySaver`, `thread_id`, `add_messages`, `get_state` |
| [`02_hitl_aprobar_plan.ipynb`](./02_hitl_aprobar_plan.ipynb) | `interrupt_before`, pausa, `update_state`, reanudar con `invoke(None)` |

Teoría: [`01_Teoria/02_HITL_guardrails_y_persistencia/`](../../01_Teoria/02_HITL_guardrails_y_persistencia/)

Prerrequisito: bloque 1 — ReAct en LangGraph.

## Dependencias

```bash
# %pip install -qU langgraph langchain-google-genai langchain-core python-dotenv
```
