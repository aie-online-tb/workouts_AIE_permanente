![Cabecera](../../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# Workout — API sobre agente cultural

El **agente LangGraph** (grafo, tools, RAG) se da por hecho: ya está en `src/`.
El centro de esta demo es **cómo adaptar un agente para que se pueda usar como API HTTP** con FastAPI.

Temática: asistente cultural para planificar tiempo en Madrid. El cliente de prueba es **Swagger** (`/docs`) — también vale Postman o cURL.

```text
/docs → FastAPI → Pydantic → procesar_turno (grafo + tools + RAG)
```

Lo nuevo que miráis aquí es la **capa HTTP**: `app.py` + `schemas.py`.

**Requisitos:** Python 3.10+ y `GEMINI_API_KEY` en `.env`.

---

## Estructura

```text
.
├── app.py                 # FastAPI: /health, /ask, /approve
├── schemas.py             # AskIn / AskOut / ApproveIn
├── config.py              # paths, modelo, defaults
├── gemini_auth.py         # carga GEMINI_API_KEY
├── src/
│   ├── agent.py           # procesar_turno, aprobar_plan
│   ├── graph.py           # StateGraph multiagente + HITL
│   ├── llm.py
│   ├── state.py
│   └── tools/             # RAG guía, API eventos, hora, cartel
├── data/
│   ├── guia_cultural.txt
│   └── eventos_fallback.json
├── assets/                # cartel_demo.jpg
├── requirements.txt
├── .env.example
└── README.md
```

Ejecuta siempre **desde esta carpeta** (donde está `app.py`).

---

## Instalación y arranque

```bash
python -m venv .venv
source .venv/bin/activate          # Git Bash / macOS / Linux
# .venv\Scripts\Activate.ps1       # Windows PowerShell

pip install -r requirements.txt
cp .env.example .env               # pega GEMINI_API_KEY
uvicorn app:app --reload --port 8000
```

---

## Swagger (`/docs`)

Con el servidor en marcha:

**http://127.0.0.1:8000/docs**

Ahí leéis la documentación generada de los endpoints y lanzáis pruebas
(*Try it out* → *Execute*).

---

## Rutas

| Método | Ruta | Qué hace |
|--------|------|----------|
| GET | `/health` | Proceso vivo (no llama al LLM) |
| POST | `/ask` | Un turno: llama a `procesar_turno` |
| POST | `/approve` | HITL: aprobar / rechazar el plan |

Base URL: `http://127.0.0.1:8000`  
Podéis ejecutar cada paso en **Swagger** (*Try it out*) o con `curl` / Postman / `requests`.

---

## Práctica guiada (flujo de peticiones)

Haced los pasos **en orden**. Usad siempre el mismo `thread_id` cuando se indique (`demo-1` o `demo-hitl`).

### 1) Comprobar que la API está viva

Haz un **GET** a `http://127.0.0.1:8000/health`.

**Respuesta esperada (200):**

```json
{
  "status": "ok"
}
```

---

### 2) Pedido completo con auto-aprobación (un solo POST)

Haz un **POST** a `http://127.0.0.1:8000/ask` enviando este JSON:

```json
{
  "pregunta": "Quiero una tarde cultural barata en el centro de Madrid: museo o exposición y algo de música si encaja. Consulta la guía y el catálogo de eventos.",
  "thread_id": "demo-1",
  "auto_aprobar": true
}
```

**Qué mirar en la respuesta (200):**

| Campo | Qué esperáis |
|-------|----------------|
| `respuesta` | Texto con un plan cultural (no vacío) |
| `thread_id` | `"demo-1"` |
| `done` | suele ser `true` (el HITL se auto-aprobó) |
| `pendiente_hitl` | `false` |

> La primera llamada puede tardar varios segundos (LLM + tools).

---

### 3) Segundo turno en el mismo hilo

Haz otro **POST** a `http://127.0.0.1:8000/ask` con el **mismo** `thread_id`:

```json
{
  "pregunta": "¿Y algo de música o jazz si encaja?",
  "thread_id": "demo-1",
  "auto_aprobar": true
}
```

**Qué mirar:** misma forma de respuesta; el hilo reutiliza el checkpointer (`demo-1`).

---

### 4) HITL manual — pedir plan sin auto-aprobar

Usad un **`thread_id` nuevo** (p. ej. `demo-hitl`) para no mezclar con el paso anterior.

Haz un **POST** a `http://127.0.0.1:8000/ask` enviando:

```json
{
  "pregunta": "Quiero una tarde cultural barata en el centro de Madrid: museo o exposición y algo de música si encaja. Consulta la guía y el catálogo de eventos.",
  "thread_id": "demo-hitl",
  "auto_aprobar": false
}
```

**Qué mirar:**

| Campo | Qué esperáis |
|-------|----------------|
| `respuesta` | Plan + aviso de que hay que aprobar/rechazar |
| `done` | `false` |
| `pendiente_hitl` | `true` |

Todavía **NO** está cerrado el plan: hace falta el siguiente endpoint.

---

### 5) Aprobar el plan (HITL)

Haz un **POST** a `http://127.0.0.1:8000/approve` enviando:

```json
{
  "thread_id": "demo-hitl",
  "aprobado": true
}
```

**Qué mirar:** `pendiente_hitl: false` y, si el grafo cierra bien, `done: true`.

*(Variante)* Repetid el paso 4 con otro `thread_id` y luego `/approve` con `"aprobado": false` → el plan no se aplica; podéis mandar otro `/ask` en ese hilo.

---

### 6) (Opcional) Cartel multimodal

Haz un **POST** a `http://127.0.0.1:8000/ask`:

```json
{
  "pregunta": "Mira el cartel de demo y úsalo si encaja con una tarde cultural en Madrid.",
  "thread_id": "demo-cartel",
  "auto_aprobar": true
}
```

**Qué mirar:** `respuesta` que mencione el cartel / evento; en código, la tool `describir_cartel` lee `assets/cartel_demo.jpg`.

---

### Errores útiles a forzar

| Qué hacer | Código | Detalle típico |
|-----------|--------|----------------|
| POST `/ask` con `"pregunta": ""` | **422** | Validación Pydantic |
| POST `/approve` con un `thread_id` que no existe | **404** | No hay sesión |
| POST `/approve` cuando no hay plan pendiente | **400** | No hay plan pendiente |

---

## Cómo leer el código

Orden sugerido:

1. **`schemas.py`** — contrato HTTP (`AskIn` / `AskOut` / `ApproveIn`).
2. **`app.py`** — traductor HTTP ↔ agente (`_sessions`, `/ask`, `/approve`).
3. **`src/agent.py`** — `procesar_turno` y `aprobar_plan` (dado; no lo reescribáis).
4. **`src/graph.py`** / **`src/tools/`** — código del agente LangGraph (viene dado. El foco es la API en este workout).

Idea clave: **FastAPI adapta; el agente decide.** `done` y `pendiente_hitl` salen de la lógica Python/LangGraph, no los inventa el LLM en el JSON de la API.

---

## Rol de ficheros

| Fichero | Responsabilidad |
|---------|-----------------|
| `app.py` | Rutas HTTP con FastAPI y sesiones por `thread_id` |
| `schemas.py` | Validación / docs del body |
| `src/agent.py` | Orquestación de turno + HITL |
| `src/graph.py` | Grafo multiagente + MemorySaver |
| `src/tools/*` | RAG guía, API Madrid, hora, cartel |
| `config.py` / `gemini_auth.py` | Paths, modelo, API key |

---

## Qué NO hace

- No reinventamos LangGraph ni las tools (el agente es el mismo que en anteriores workouts).
- El cliente de esta demo es `/docs` y **swagger** (no hay UI propia) o herramientas como **Postman** o **cURL**.
- Al reiniciar `uvicorn` se pierden las sesiones en RAM (el checkpointer también es en memoria). No hay persistencia de datos en esta demo.

---

## Mini glosario

| Término | Qué significa aquí |
|---------|-------------------|
| **Adaptar** | Exponer `procesar_turno` detrás de HTTP, sin reescribir el grafo. |
| **`thread_id`** | Identificador de conversación (sesión API + checkpointer). |
| **`auto_aprobar`** | Atajo de demo: aprueba el HITL dentro de `/ask`. |
| **`/approve`** | HITL explícito (aprobar / rechazar). |
| **`pendiente_hitl`** | El grafo espera decisión humana. |
| **`done`** | Turno/plan cerrado según la lógica del agente. |

---

## Checklist

- [ ] Arranqué con `.env` y vi `/docs`.
- [ ] `/ask` con pedido cultural devolvió una respuesta del agente.
- [ ] Probé `auto_aprobar: true` (flujo de un paso).
- [ ] Probé `auto_aprobar: false` + `/approve`.
- [ ] Entiendo que `app.py` es fino: la lógica del agente está en `src/`.