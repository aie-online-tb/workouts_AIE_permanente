# Guion — Estado y memoria en conversación

**Material:** `01_estado_y_memoria_del_agente.ipynb`  
**Duración:** ~10–12 min

---

## Apertura (~45 s)
- Idea: un **dict** recuerda preferencias entre mensajes.
- Frase: *LLM propone JSON; Python guarda y decide `done`.*

## Setup (~1 min)
- Instalar, API key, modelo.

## Estado (~2 min)
- `crear_estado` + `tenemos_datos_minimos`.
- Obligatorios: intereses, presupuesto, zona. Duración opcional (si falta, la sugiere el LLM).

## leer_json / actualizar_estado / calcular_done (~4 min)
- Una función por celda.
- Insistir: `deepcopy`, merge de preferencias, **`done` lo calcula Python** (no viene del JSON).

## preguntar_al_modelo (~1,5 min)
- Prompt corto: preguntar o planificar. Sin campo `done`.

## Ejecutar 4 turnos (~3 min)
1. tarde cultural → pregunta  
2. cine/música barato → guarda prefs  
3. zona centro → casi listo  
4. sí, 3 horas → plan → `calcular_done` pone `done=True`

## Cierre (~30 s)
- Chat vs estado.
- Puente a Bloque 3.
