# Workout — Function calling (`hora_actual`)

Guion vivo del notebook `01_tool_use_hora_actual.ipynb`.

## Objetivo

Function calling de **dos formas**:

1. **Manual** — el alumno ve pedir → ejecutar → devolver → texto.
2. **Automático (AFC)** — el SDK hace ese ciclo por dentro.

**Aún no es un agente**: no hay estado, ni varias tools, ni `done`. Solo modelo + una función.

## Guion de clase (~25–30 min)

1. Dejar claro: el LLM **no ejecuta** código; solo **pide**. Python ejecuta (a mano o vía SDK).
2. Probar `hora_actual()` sin Gemini.
3. Declarar la tool y **desactivar AFC**.
4. Ciclo manual A → B → C en voz alta.
5. Activar AFC (`tools=[hora_actual]`): misma idea, loop oculto.
6. Checklist (manual + automático).

## Mensaje para llevar

Misma idea en ambos modos: el LLM pide; Python ejecuta; el resultado vuelve al modelo.  
Cambia quién orquesta el ciclo (tú vs SDK), no quién corre el código.
