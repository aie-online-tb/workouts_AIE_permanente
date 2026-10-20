![Cabecera](../../../../../06_AI_Agents_Engineering/Sprint_11/assets/cabecera_thebridge.png)

# Workout B1 — Primera API FastAPI (CRUD + Pydantic)

Gimnasio HTTP: **FastAPI + Pydantic** con un CRUD de ítems en memoria.

- métodos **GET / POST / PUT / DELETE**
- validación con **Pydantic** (`Field`, `Path`, `Query` → 422)

La lista vive en **RAM**: al reiniciar `uvicorn` vuelven los 3 ítems de ejemplo.

```text
cliente (/docs o curl) → FastAPI (rutas) → Pydantic (contrato) → lista en memoria
```

---

## Estructura

```text
.
├── app.py             # rutas CRUD + HTTPException
├── schemas.py         # contrato Item (Pydantic)
├── requirements.txt
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
uvicorn app:app --reload --port 8000
```

---

## Swagger (`/docs`)

Con el servidor en marcha, abre el navegador en:

**http://127.0.0.1:8000/docs**

Eso es **Swagger UI**: la documentación interactiva que FastAPI genera solo a partir de tus rutas y schemas Pydantic.

Sirve para:

1. **Leer la documentación** de cada endpoint (método, path, query/path params, body, códigos de respuesta).
2. **Probar la API sin curl ni Postman**: expandís un endpoint → *Try it out* → rellenáis parámetros/body → *Execute*.

Es el cliente principal de este workout: toda la práctica de abajo se hace desde ahí.

(Alternativa: `http://127.0.0.1:8000/redoc` — misma info, solo lectura, sin botón de prueba.)

---

## Rutas

| Método | Ruta | Qué hace |
|--------|------|----------|
| GET | `/items` | Listar (`skip`, `limit`, `on_offer`) |
| GET | `/items/{item_id}` | Un ítem |
| POST | `/items` | Crear (201; 409 si el id existe) |
| PUT | `/items/{item_id}` | Sustituir |
| DELETE | `/items/{item_id}` | Borrar (204) |

Base URL: `http://127.0.0.1:8000`  
Podéis ejecutar cada paso en **Swagger** (*Try it out*) o con `curl` / Postman / `requests`.

---

## Práctica guiada (flujo de peticiones)

Haced los pasos **en orden**. Al crear el ítem `id: 10`, usad ese id en PUT / DELETE.

### 1) Listar ítems

Haz un **GET** a `http://127.0.0.1:8000/items`.

**Respuesta esperada (200):** lista con los 3 ítems de ejemplo (`Laptop`, `Smartphone`, `Auriculares`).

---

### 2) Filtrar por oferta y paginar

Haz un **GET** a `http://127.0.0.1:8000/items?on_offer=true`.

**Qué mirar:** solo ítems con `"on_offer": true` (p. ej. Laptop y Auriculares).

Probad también:

- `http://127.0.0.1:8000/items?skip=0&limit=2` → como máximo 2 ítems  
- `http://127.0.0.1:8000/items?skip=1&limit=1` → 1 ítem, saltando el primero  

---

### 3) Obtener un ítem por id

Haz un **GET** a `http://127.0.0.1:8000/items/1`.

**Respuesta esperada (200):** el objeto `Laptop` (o el ítem con `id: 1`).

---

### 4) Ítem que no existe → 404

Haz un **GET** a `http://127.0.0.1:8000/items/99`.

**Respuesta esperada (404):**

```json
{
  "detail": "Ítem no encontrado"
}
```

---

### 5) Crear un ítem

Haz un **POST** a `http://127.0.0.1:8000/items` enviando este JSON:

```json
{
  "id": 10,
  "name": "Teclado",
  "description": "Mecánico",
  "price": 79.9,
  "on_offer": true
}
```

**Respuesta esperada (201):** el mismo objeto (o equivalente) que enviasteis.

Comprobad con **GET** `http://127.0.0.1:8000/items/10` → 200 y el teclado.

---

### 6) Id duplicado → 409

Haz otro **POST** a `http://127.0.0.1:8000/items` con el **mismo** body del paso 5.

**Respuesta esperada (409):**

```json
{
  "detail": "Ya existe un ítem con ese id"
}
```

---

### 7) Datos inválidos → 422 (Pydantic)

Haz un **POST** a `http://127.0.0.1:8000/items` enviando:

```json
{
  "id": 11,
  "name": "Raton",
  "description": "Inalámbrico",
  "price": -1,
  "on_offer": false
}
```

**Qué mirar:** código **422**; en `detail` Pydantic explica que `price` debe ser mayor que 0.

Variante: `"name": ""` → también **422** (`min_length`).

> El 422 lo genera Pydantic automáticamente; no hace falta un `if` manual en la ruta.

---

### 8) Sustituir un ítem (PUT)

Haz un **PUT** a `http://127.0.0.1:8000/items/10` enviando:

```json
{
  "id": 10,
  "name": "Teclado",
  "description": "Mecánico RGB",
  "price": 89.9,
  "on_offer": false
}
```

**Importante:** el `id` del body debe coincidir con el de la URL (`10`).

**Respuesta esperada (200):** el ítem actualizado (`price: 89.9`, `on_offer: false`).

Comprobad con **GET** `http://127.0.0.1:8000/items/10` → **200** y el ítem editado (`price: 89.9`, `on_offer: false`).

*(Variante)* Si el `id` del body ≠ el de la URL → **400** (`El id del body debe coincidir con el de la URL`).

---

### 9) Borrar un ítem (DELETE)

Haz un **DELETE** a `http://127.0.0.1:8000/items/10`.

**Respuesta esperada (204):** sin cuerpo (en Swagger suele verse vacío).

Comprobad con **GET** `http://127.0.0.1:8000/items/10` → **404**.

---

### Errores útiles a forzar

| Qué hacer | Código | Detalle típico |
|-----------|--------|----------------|
| GET `/items/99` | **404** | Ítem no encontrado |
| POST mismo `id` dos veces | **409** | Ya existe un ítem con ese id |
| POST con `price: -1` o `name: ""` | **422** | Validación Pydantic |
| PUT con id URL ≠ id body | **400** | Ids no coinciden |

---

## Cómo leer el código

Orden sugerido:

1. **`schemas.py`** — contrato `Item` (`Field`: rangos, longitudes, opcionales).
2. **`app.py`** — lista en memoria → GET → POST → PUT → DELETE.
3. Fíjate en `Path` vs `Query`, `response_model` y los `HTTPException` (404 / 409 / 400).

Idea clave: **Pydantic valida la forma de los datos; la ruta decide la lógica de negocio** (existe / no existe / conflicto).

---

## Rol de ficheros

| Fichero | Responsabilidad |
|---------|-----------------|
| `schemas.py` | Qué puede entrar/salir (`Item`) |
| `app.py` | Endpoints, filtros, errores HTTP |
| `requirements.txt` | Dependencias (`fastapi`, `uvicorn`, `pydantic`) |

---

## Qué NO hace

- No hay base de datos (solo una lista de Python).
- No hay autenticación ni API keys.
- No hay UI aparte de `/docs`.

---

## Mini glosario

| Término | Qué significa aquí |
|---------|-------------------|
| **`Field`** | Reglas del campo en el schema (obligatorio, `gt`, `min_length`…). |
| **`Path`** | Parámetro en la URL: `/items/{item_id}`. |
| **`Query`** | Parámetro tras `?`: `/items?skip=0&limit=10`. |
| **`response_model`** | Forma esperada del JSON de salida (y docs). |
| **`HTTPException`** | Error HTTP controlado (404, 409…). |
| **422** | Body/query inválidos según Pydantic (automático). |

---

## Checklist

- [ ] Probé GET, POST, PUT y DELETE en Swagger.
- [ ] Probé `skip` / `limit` y el filtro `on_offer`.
- [ ] Vi un **422** al mandar datos inválidos (validación Pydantic).
- [ ] Vi un **404** (no existe) y un **409** (id duplicado).
- [ ] Entiendo que al reiniciar `uvicorn` se pierden los cambios.
