# Guion — HITL: aprobar plan

**Material:** `02_hitl_aprobar_plan.ipynb`  
**Duración:** ~12–15 min

## Apertura

- No todo lo que propone el LLM debe ejecutarse sin revisión.
- Patrón: **pausar** el grafo, mostrar plan, decidir, **reanudar**.

## Contenido

1. Grafo lineal `proponer → aplicar` con estado `plan` / `aprobado` / `resultado`.
2. `interrupt_before=["aplicar"]` + checkpointer obligatorio.
3. Primer `invoke`: `snap.next` incluye `aplicar`; plan visible, `resultado` vacío.
4. Aprobar: `update_state({"aprobado": True})` + `invoke(None, config=…)`.
5. Rechazar con otro `thread_id`: misma pausa, decisión distinta.
6. Puente al proyecto cultural: botones en Streamlit, mismo hilo.

## Cierre

- Tabla `interrupt_before` / `update_state` / `invoke(None)`.
- Python decide si aplicar según `aprobado`; el LLM solo propone el plan.
- Anunciar bloque 3: multiagente corto y multimodal intro.
