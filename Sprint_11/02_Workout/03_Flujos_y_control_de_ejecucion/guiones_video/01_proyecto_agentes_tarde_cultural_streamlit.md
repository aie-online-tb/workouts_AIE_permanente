# Guion — Flujos y control de ejecución · Streamlit

**Material:** `05_proyecto_agentes_tarde_cultural_streamlit/` (proyecto Python)

**Duración aproximada:** ~10–12 min

---

## Apertura (~45 s)

- Workout anterior (`01_estado_y_memoria_del_agente`): conversación + AgentState + `done` en Python.
- Este workout: **empaquetar** en módulos + CLI + Streamlit.
- Frase clave: *`procesar_turno(estado, mensaje)` es el contrato; CLI y Streamlit son clientes*.

## Estructura del proyecto (~2 min)

- Raíz: `main`, `app`, `config`, `gemini_auth`.
- `src/`: `agent`, `llm`, `state` (backend del agente).
- Ejecutar siempre desde la raíz.

## `procesar_turno` — un turno con control (~2,5 min)

- Validación mensaje vacío.
- Flujo: LLM → `actualizar_estado` → `calcular_done` (Python decide `done`).
- `try/except`: error → `state["error"]` + entrada en `traza` con `status: "error"`.
- `run_demo`: bucle de mensajes con tope `max_turns`; mensaje fallback si no hay `done`.

## CLI con `main.py` (~1,5 min)

- `python main.py` — guion demo de 5 turnos → resumen + JSON.
- `python main.py --max-turns 2` — corte visible (solo 2 de 5).
- `python main.py --interactivo` — chat turno a turno.
- Señalar resumen (`corte: max_turns`) y `traza` en el JSON.

## Streamlit `app.py` (~2,5 min)

- Chat: `st.session_state.messages`, `st.chat_input`.
- Diferencia clave: **`agent_state` en sesión**; cada mensaje llama **`procesar_turno`**.
- Sidebar: slider `max_turns`, botón «Nueva conversación».
- Plan borrador vs plan final; expander debug (no confundir con historial de chat).

## Cierre (~30 s)

- Apuntar a `02_proyecto_agentes_tarde_cultural_streamlit.md` y carpeta teoría `05_proyecto_agentes_tarde_cultural_streamlit/`.
- Práctica live review: completar `agent_starter.py`.
