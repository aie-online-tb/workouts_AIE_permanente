![Cabecera](../../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# Workout — API sobre agente + historial (SQLModel / SQLite)

**Qué aprendéis:** cablear **SQLModel + SQLite** detrás de FastAPI — guardar el turno tras `/ask` y leerlo (endpoint + fichero `.db`). El agente en `src/` es el contexto; el foco es la **persistencia**.

API FastAPI sobre un **agente cultural** LangGraph (`/health`, `/ask`, `/approve`) con **historial persistente** en SQLite (SQLModel).

Tras un turno cerrado, Python guarda pregunta + respuesta. Podéis listar el historial y comprobar que **sobrevive** a reiniciar `uvicorn`.

```text
/docs → FastAPI → procesar_turno → save_turn (historial.db)
                 → GET /threads/{id}/messages
```

**Requisitos:** Python 3.10+ y `GEMINI_API_KEY` en `.env`.

---

## Estructura

```text
.
├── app.py                 # FastAPI: /health, /ask, /approve + historial
├── schemas.py             # AskIn / AskOut / ApproveIn / MessageOut
├── config.py              # paths, modelo, DATABASE_URL → historial.db
├── gemini_auth.py         # carga GEMINI_API_KEY
├── src/
│   ├── agent.py           # procesar_turno, aprobar_plan
│   ├── graph.py           # StateGraph multiagente + HITL
│   ├── llm.py
│   ├── state.py
│   ├── tools/             # RAG guía, API eventos, hora, cartel
│   ├── models.py          # Conversation, Message (SQLModel)
│   └── db.py              # ensure_schema, save_turn, list_messages
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

Al arrancar se crea `historial.db` si no existe.

---

## Ver la base de datos (`historial.db`)

Además del GET `/threads/{id}/messages`, podéis **abrir el fichero** en VS Code / Cursor
con una extensión de SQLite (por ejemplo *SQLite Viewer*):
clic derecho en `historial.db` → **Open With** → la extensión.

Tablas a mirar: `conversation` y `message` (filas `user` / `assistant` tras cada `/ask`).
Así contrastáis lo que ve la API con lo que hay guardado en SQLite.

---

## Swagger (`/docs`)

Con el servidor en marcha:

**http://127.0.0.1:8000/docs**

Ahí leéis la documentación generada con **Swagger** de los endpoints y podéis lanzar pruebas.

---

## Rutas

| Método | Ruta | Qué hace |
|--------|------|----------|
| GET | `/health` | Proceso vivo + `"storage": "sqlite"` |
| POST | `/ask` | Un turno; si cierra, guarda en SQLite |
| POST | `/approve` | HITL; si cierra, también puede guardar |
| GET | `/threads/{thread_id}/messages` | Historial SQL del hilo |

Base URL: `http://127.0.0.1:8000`  
Podéis ejecutar cada paso en **Swagger** o con `curl` / Postman / `requests`.

---

## Práctica guiada. Flujo de peticiones para comprobar la API

Haced los pasos **en orden**. Usad el mismo `thread_id` (`demo-db`) en los pasos de historial.

> **Tiempo de `/ask`:** no es un CRUD rápido. El agente hace varios saltos al LLM + tools
> (guía, eventos, etc.), así que **cada `/ask` puede tardar del orden de 1–3 minutos**.
> Esperad a que Swagger termine (*Execute*); `/health` y `GET …/messages` sí son instantáneos.
> El foco de este workout es la **persistencia** del historial, no la latencia del agente.

### 1) Comprobar que la API está viva

Haz un **GET** a `http://127.0.0.1:8000/health`.

**Respuesta esperada (200):**

```json
{
  "status": "ok",
  "storage": "sqlite"
}
```

---

### 2) Primer `/ask` (con auto-aprobar:true, sin HITL)

Haz un **POST** a `http://127.0.0.1:8000/ask`:

```json
{
  "pregunta": "Quiero una tarde cultural barata en el centro de Madrid: museo o exposición y algo de música si encaja. Consulta la guía y el catálogo de eventos.",
  "thread_id": "demo-db",
  "auto_aprobar": true
}
```

**Qué mirar en la respuesta (200):**

| Campo | Qué esperáis |
|-------|----------------|
| `respuesta` | Texto con un plan cultural (no vacío) |
| `thread_id` | `"demo-db"` |
| `done` | suele ser `true` |
| `pendiente_hitl` | `false` |

> Tras cerrar el turno, Python llama a `save_turn` (eso es rápido; lo lento es el agente).

---

### 3) Segundo `/ask` (mismo hilo)

Haz otro **POST** a `http://127.0.0.1:8000/ask`:

```json
{
  "pregunta": "¿Y algo de jazz si encaja?",
  "thread_id": "demo-db",
  "auto_aprobar": true
}
```

**Qué mirar:** misma forma de respuesta; se guarda otro turno en el mismo hilo.

---

### 4) Leer historial SQL

Haz un **GET** a `http://127.0.0.1:8000/threads/demo-db/messages`.

**Qué mirar:** lista de mensajes `user` / `assistant` (tras 2 turnos → **4** filas).

Hasta aquí el agente ha respondido; ahora miramos la **base de datos**.
Abrid también `historial.db` con *SQLite Viewer* y comprobad las tablas `conversation` / `message`.

---

### 5) Reiniciar y comprobar persistencia

1. Parad `uvicorn` (Ctrl+C).
2. Volved a arrancar: `uvicorn app:app --reload --port 8000`
3. Repetid el **GET** `http://127.0.0.1:8000/threads/demo-db/messages`

**Qué mirar:** los mismos mensajes siguen (vienen de `historial.db`, no de la RAM del agente).

Tras reiniciar, abrid otra vez `historial.db`: las filas siguen ahí (no solo en `/docs`).

---

### 6) HITL manual

`/ask` con `"auto_aprobar": false` → `/approve`.
Cuando el plan cierra, también se escribe en SQLite.

---

### Errores útiles a forzar

| Qué hacer | Código | Detalle típico |
|-----------|--------|----------------|
| POST `/ask` con `"pregunta": ""` | **422** o **400** | Validación / pregunta vacía |
| POST `/approve` con un `thread_id` que no existe | **404** | No hay sesión |
| POST `/approve` cuando no hay plan pendiente | **400** | No hay plan pendiente |

---

## Cómo leer el código

Orden sugerido:

1. **`src/models.py` / `src/db.py`** — historial (`Conversation` / `Message`, `save_turn`).
2. **`app.py`** — rutas HTTP + `_persistir_si_hay_respuesta` y `GET …/messages`.
3. **`schemas.py`** — contrato HTTP (`AskIn` / `AskOut` / `MessageOut`).
4. **`src/agent.py`** — orquestación del turno (`procesar_turno`, `aprobar_plan`).
5. **`src/graph.py` / `src/tools/`** — grafo LangGraph y tools (si queréis bajar al agente).

Idea clave: **el agente responde; SQL guarda el rastro.** El checkpointer LangGraph en RAM ≠ historial SQL.

---

## Rol de ficheros

| Fichero | Responsabilidad |
|---------|-----------------|
| `app.py` | Rutas HTTP; tras el turno llama a `save_turn` |
| `schemas.py` | Validación / docs del body y del historial |
| `src/models.py` | Tablas SQLModel del historial |
| `src/db.py` | Engine, schema, `save_turn`, `list_messages` |
| `src/agent.py` | Orquestación de turno + HITL |
| `src/graph.py` / `src/tools/*` | Grafo LangGraph y tools |
| `config.py` / `gemini_auth.py` | Paths, `DATABASE_URL`, API key |

---

## Qué NO hace

- No persiste el checkpointer completo de LangGraph.
- Al reiniciar, las sesiones del grafo en RAM se pierden; el **historial SQL** no.
- El cliente de esta demo es `/docs` (Swagger), Postman o cURL.

---

## Mini glosario

| Término | Qué significa aquí |
|---------|-------------------|
| **`save_turn`** | Escribe user + assistant en SQLite tras un turno cerrado. |
| **`thread_id`** | Id de conversación (sesión API + filas en `historial.db`). |
| **`historial.db`** | Fichero SQLite local (se crea al arrancar). |
| **Checkpointer** | Memoria del grafo en RAM; no es el historial SQL. |
| **`done` / `pendiente_hitl`** | Flags del agente; salen de la lógica Python/LangGraph, no del ORM. |

---

## Checklist

- [ ] Arranqué con `.env` y vi `/docs`.
- [ ] `/health` muestra `"storage": "sqlite"`.
- [ ] Dos `/ask` + GET messages → 4 filas.
- [ ] Abrí `historial.db` y vi las tablas `conversation` / `message`.
- [ ] Tras reiniciar uvicorn, el historial sigue.
- [ ] Entiendo `save_turn` en `src/db.py`.
