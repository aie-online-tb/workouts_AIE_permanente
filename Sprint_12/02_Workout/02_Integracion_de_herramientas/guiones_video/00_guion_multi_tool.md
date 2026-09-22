# Workout — Integración de herramientas

Guion vivo del notebook `01_multi_tool_con_rag.ipynb`.

## Objetivo

Modularizar tools en `tools/`, retrieve mínimo como RAG-tool, API con fallback. Loop multi-tool con allowlist. El **modelo** elige la tool.

## Guion de clase (~40–45 min)

1. Árbol `config.py` + `tools/` + `data/`.
2. Probar sin Gemini: `hora_actual`, `RAG_buscar_en_guia`, `API_consultar_eventos_madrid`.
3. Explicar RAG (retrieve mínimo, no pipeline completo) y API (GET → N → resumen / fallback).
4. Declarar 3 tools (contrato Gemini) + loop (`run_con_tools`, AFC off, `max_steps` como freno).
5. Mensaje clave: no hay `if` de routing; Gemini elige por `description` + pregunta.
6. Preguntas: solo hora → solo RAG → solo API → guía+hora → allowlist.
7. (Opcional, 2 min) AFC con 3 tools: misma pregunta que 5.4; no hay `--- step N`.
8. Checklist + puente: esto es el loop; el agente completo es el proyecto B3.

## Mensaje para llevar

Las tools viven en módulos; el notebook orquesta. El modelo decide qué tool; Python ejecuta solo la allowlist. El agente completo (CLI, estado, `done`) es el proyecto del bloque 3.
