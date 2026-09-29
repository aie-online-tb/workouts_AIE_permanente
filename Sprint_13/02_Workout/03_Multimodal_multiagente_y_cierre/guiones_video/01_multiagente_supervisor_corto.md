# Guion — Multiagente con supervisor (overview básico)

**Material:** `01_multiagente_supervisor.ipynb`  
**Duración:** ~18–22 min

## Apertura (~2 min)

- Multiagente aquí = **varios nodos + estado compartido + orquestación**, no equipos en paralelo.
- Objetivo del notebook: overview **básico completo** (no solo “clasificar y listo”).

## Contenido

1. Estado: `pedido`, `notas_cultura`, `notas_practico`, `respuesta`, `siguiente`, `iteracion`, `log` (reducer).
2. Supervisor: elige `cultura` / `practico` / `sintetizar` / `FINISH` + fallback Python + `MAX_ITER`.
3. Especialistas: cultura y practico escriben notas; sintetizar **lee ambas**.
4. Grafo: conditional edges + **vuelta al supervisor** (el bucle) + `MemorySaver` + `draw_ascii()`.
5. Dos `invoke` con **`thread_id` distintos** (museo/centro vs música/Lavapiés); `get_state` del primer hilo.

## Cierre (~2 min)

- Tabla de piezas (estado, supervisor, router, bucle, FINISH).
- El proyecto del sprint **no** usa este patrón: ReAct + HITL basta.
- Anunciar multimodal (imagen + texto).
