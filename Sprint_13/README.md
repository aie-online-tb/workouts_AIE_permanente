![Cabecera](../Sprint_11/assets/cabecera_thebridge.png)

# 📘 Sprint 13 — Autonomous Agent Systems

En el Sprint 11 el agente mantuvo **estado** y `done`. En el Sprint 12 usó **tools** con control y practicasteis la **API básica** de LangGraph (grafo lineal + condicionales).

Aquí el salto: **orquestar el agente con LangGraph** (bucle LLM ↔ tools), añadir **persistencia / HITL**, y cerrar el módulo con una intro a **multi-agente** y **multimodal**.

> **¿Cómo orquesto el agente con LangGraph, con autonomía controlada (HITL + límites), sin perder lo aprendido en S11–S12?**

---

## Mapa del módulo (Sprints 11–13)

| Sprint | Pregunta | Fase |
|--------|----------|------|
| **11** | ¿Qué es un agente y cómo mantiene estado? | Fundamentos |
| **12** | ¿Cómo actúa con herramientas (+ RAG)? | Tool use + LangGraph básico |
| **13** (este) | ¿Cómo planifica con autonomía controlada? | LangGraph (proyecto) + HITL + intros |

```text
S11  mensaje → procesar_turno → estado + done + max_turns
 ↓
S12  + tools (allowlist, max_steps) + notebooks LangGraph (lineal / router)
 ↓
S13  mismo agente → grafo (ReAct) + checkpoints + HITL
     + intro multi-agente / multimodal
     → Project Break 2
```

**Prerrequisito:** haber hecho S12 (proyecto tools y/o Live Review + notebooks `04_LangGraph_basico`).  
**No repetimos** en este sprint los notebooks 01/02 de LangGraph básico (ya están en S12).

---

## Stack y dominio

- **Stack:** Python + Gemini + LangGraph · Streamlit · **sin AWS Bedrock**
- **Proyecto / workouts:** tarde cultural (migración del agente S12)
- **Live Review:** calidad del aire (mismo patrón, otro dominio)

---

## 🧭 Bloque 1 — Orquestación LangGraph con tools

📁 [`01_Teoria/01_Orquestacion_LangGraph_con_tools/`](./01_Teoria/01_Orquestacion_LangGraph_con_tools/)

> De `run_tool_loop` (while) al **StateGraph**: nodos agent/tools, bucle ReAct, control en Python.

| Workout | Descripción |
|---------|-------------|
| [01_agente_tools_en_langgraph.ipynb](./02_Workout/01_Orquestacion_LangGraph_con_tools/01_agente_tools_en_langgraph.ipynb) | ReAct en LangGraph |

---

## 🛡️ Bloque 2 — HITL, guardrails y persistencia

📁 [`01_Teoria/02_HITL_guardrails_y_persistencia/`](./01_Teoria/02_HITL_guardrails_y_persistencia/)

> Checkpoints, `thread_id`, memoria de mensajes, **aprobación humana**, límites en el grafo.

| Workout | Descripción |
|---------|-------------|
| [01_memoria_y_checkpoints.ipynb](./02_Workout/02_HITL_guardrails_y_persistencia/01_memoria_y_checkpoints.ipynb) | MemorySaver + thread_id |
| [02_hitl_aprobar_plan.ipynb](./02_Workout/02_HITL_guardrails_y_persistencia/02_hitl_aprobar_plan.ipynb) | HITL aprobar plan |

---

## 🧩 Bloque 3 — Multi-agente / multimodal (intro) + proyecto

📁 [`01_Teoria/03_Multimodal_multiagente_y_cierre/`](./01_Teoria/03_Multimodal_multiagente_y_cierre/)

> Intro multi-agente y multimodal; Streamlit como cliente del grafo; **proyecto hito**.

📁 Proyecto: [`05_proyecto_agente_langgraph_tarde_cultural/`](./01_Teoria/03_Multimodal_multiagente_y_cierre/05_proyecto_agente_langgraph_tarde_cultural/)

| Workout | Descripción |
|---------|-------------|
| [01_multiagente_supervisor.ipynb](./02_Workout/03_Multimodal_multiagente_y_cierre/01_multiagente_supervisor.ipynb) | Overview multiagente (bucle + MemorySaver) |
| [02_multimodal_imagen_texto.ipynb](./02_Workout/03_Multimodal_multiagente_y_cierre/02_multimodal_imagen_texto.ipynb) | LangGraph + imagen → texto |

---

## 🎯 Practica live review

📁 [`Practica_live_review/`](./Practica_live_review/) — agente LangGraph · **calidad del aire** (alumno + SOLUTION).

Mismas mecánicas que el proyecto cultural; otro dominio. TODOs: cablear grafo (tools loop) y/o HITL + `procesar_turno`.

---

## Escalera pedagógica

```text
Notebook: tools en LangGraph (ReAct)
    ↓
Notebook: memoria / checkpoints
    ↓
Notebook: HITL (aprobar plan)
    ↓
Proyecto cultural LangGraph + Streamlit
    ↓
Live Review calidad del aire
    ↓
Intro multi-agente + multimodal (cierre)
    ↓
Project Break 2
```

---

## Fuera de alcance

AWS Bedrock · ciberseguridad avanzada · LangSmith a fondo · multi-agente de producción · repetir grafos lineales/condicionales básicos de S12.

## Estado

| Pieza | Estado |
|-------|--------|
| Teoría B1–B3 | Completada (intros) |
| Notebooks ReAct / memoria / HITL / multi / multimodal | Completados |
| Proyecto cultural LangGraph + HITL + Streamlit | Implementado |
| Live Review aire (alumno + SOLUTION) | Completada |
