"""
Workout B1 — CRUD en memoria con FastAPI + Pydantic.

Idea: practicar GET / POST / PUT / DELETE y ver cómo Pydantic valida.
Los datos viven en una lista de Python (no hay base de datos todavía).
Al reiniciar uvicorn, la lista vuelve al estado inicial de abajo.

Arranque:
  uvicorn app:app --reload --port 8000
  → http://127.0.0.1:8000/docs
"""

from typing import List, Optional

from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import RedirectResponse

from schemas import Item  # el contrato Pydantic (Field, validaciones)

# Instancia de la aplicación. title/description salen en /docs
app = FastAPI(
    title="Primera API FastAPI",
    description="CRUD de ítems en memoria. Practicad GET/POST/PUT/DELETE en /docs.",
)

# "Base de datos" falsa: lista en RAM para probar la API (se pierde al reiniciar)
items_db: List[Item] = [
    Item(
        id=1,
        name="Laptop",
        description="Portátil para desarrollo",
        price=1200.99,
        on_offer=True,
    ),
    Item(
        id=2,
        name="Smartphone",
        description="Teléfono de gama media",
        price=899.99,
        on_offer=False,
    ),
    Item(
        id=3,
        name="Auriculares",
        description="Cancelación de ruido",
        price=199.99,
        on_offer=True,
    ),
]


def _find_index(item_id: int) -> int:
    """Devuelve la posición en items_db, o -1 si no existe."""
    for i, item in enumerate(items_db):
        if item.id == item_id:
            return i
    return -1


@app.get("/", include_in_schema=False)
def root():
    """La raíz no tiene contenido propio: manda a la documentación Swagger."""
    return RedirectResponse(url="/docs")


# --- GET: leer ---------------------------------------------------------------

@app.get("/items", response_model=List[Item])
def list_items(
    # Query(...) = parámetros de la URL tras ?  →  /items?skip=0&limit=10&on_offer=true
    skip: int = Query(0, ge=0, description="Cuántos ítems saltar"),
    limit: int = Query(10, ge=1, le=100, description="Máximo de ítems a devolver"),
    # Optional[bool] = booleano opcional: None = no filtrar; True/False = filtrar
    on_offer: Optional[bool] = Query(None, description="Filtrar por oferta"),
):
    """Listar ítems. response_model documenta/filtra la forma del JSON de salida."""
    data = items_db

    # Si el cliente envió on_offer, nos quedamos solo con los que coinciden
    if on_offer is not None:
        filtrados = []
        for item in data:
            if item.on_offer == on_offer:
                filtrados.append(item)
        data = filtrados

    # slicing de lista: paginación simple
    return data[skip : skip + limit]


@app.get("/items/{item_id}", response_model=Item)
def get_item(
    # Path(...) = trozo de la URL  →  /items/2
    item_id: int = Path(..., ge=1, description="ID del ítem"),
):
    """Obtener un ítem por id. Si no está → 404."""
    idx = _find_index(item_id)
    if idx < 0:
        # HTTPException = respuesta de error con código HTTP
        raise HTTPException(status_code=404, detail="Ítem no encontrado")
    return items_db[idx]


# --- POST: crear -------------------------------------------------------------

@app.post("/items", response_model=Item, status_code=201)
def create_item(item: Item):
    """
    Crear un ítem.
    `item: Item` = el body JSON se valida contra el schema (fallo → 422 automático).
    status_code=201 = "creado" (en lugar del 200 por defecto).
    """
    if _find_index(item.id) >= 0:
        # 409 Conflict: el recurso ya existe
        raise HTTPException(status_code=409, detail="Ya existe un ítem con ese id")
    items_db.append(item)
    return item


# --- PUT: sustituir ----------------------------------------------------------

@app.put("/items/{item_id}", response_model=Item)
def update_item(item: Item, item_id: int = Path(..., ge=1)):
    """Sustituir el ítem. El id de la URL y el del body deben coincidir."""
    idx = _find_index(item_id)
    if idx < 0:
        raise HTTPException(status_code=404, detail="Ítem no encontrado")
    # 400 = petición mal formada (ids distintos)
    if item.id != item_id:
        raise HTTPException(
            status_code=400,
            detail="El id del body debe coincidir con el de la URL",
        )
    items_db[idx] = item
    return item


# --- DELETE: borrar ----------------------------------------------------------

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int = Path(..., ge=1)):
    """
    Borrar por id.
    204 = OK sin cuerpo de respuesta (por eso return None).
    """
    idx = _find_index(item_id)
    if idx < 0:
        raise HTTPException(status_code=404, detail="Ítem no encontrado")
    del items_db[idx]
    return None
