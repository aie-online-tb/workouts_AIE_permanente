# Guion — Memoria y checkpoints

**Material:** `01_memoria_y_checkpoints.ipynb`  
**Duración:** ~12–15 min

## Apertura

- Sin checkpointer, cada `invoke` olvida lo anterior.
- En producción (Streamlit) necesitáis un **hilo** estable por conversación.

## Contenido

1. Chat mínimo: un nodo + `add_messages`.
2. `MemorySaver` al compilar.
3. `configurable.thread_id`: Ana recuerda nombre y gustos en el turno 2.
4. Bob en otro hilo: no ve a Ana.
5. `get_state`: inspeccionar mensajes acumulados.
6. Mención breve de `SqliteSaver` para disco (opcional).

## Cierre

- Tabla `MemorySaver` / `thread_id` / `get_state`.
- Enlace con UI: mismo `thread_id` que la sesión de chat.
- Anunciar notebook HITL (aprobar plan).
