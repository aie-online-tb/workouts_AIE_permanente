# Guion vídeo — Proyecto agente tools

1. Estructura: raíz (`main`, `app`, `config`, `gemini_auth`) vs `src/` (agente + `tools/`) + allowlist.
2. Demo CLI completa: `python main.py` (5 mensajes de `DEMO_MENSAJES`) → resumen + JSON / `traza`.
3. Límites con valor visible:
   - `python main.py --max-turns 2` → corte por turnos (solo 2 de 5).
   - `python main.py --max-turns 1 --max-steps 1` → corte por steps (mensaje de max_steps).
4. Señalar `traza[].tools` (`step`, `tool`, `args`, `status`, `preview`).
5. Streamlit: mismo backend, plan borrador antes de `done`, expander debug.
6. (Opcional) Fallback: Wi‑Fi off → `Fuente: fallback` en la traza.
7. Cierre: `max_steps` ≠ `max_turns`; `done` lo calcula el agente (no es una tool).
