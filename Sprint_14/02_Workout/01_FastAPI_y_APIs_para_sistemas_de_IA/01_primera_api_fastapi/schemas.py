"""
Contratos de datos con Pydantic.

FastAPI usa estas clases para:
- validar el JSON que llega (body) o documentar respuestas,
- rechazar datos inválidos con HTTP 422,
- generar la documentación de /docs (Swagger).

`BaseModel` = "este es un esquema".
`Field(...)` = reglas extra sobre cada campo (obligatorio, rangos, textos de ayuda).
"""

from typing import Optional

from pydantic import BaseModel, Field


class Item(BaseModel):
    """Un producto/ítem de la API de ejemplo (CRUD en memoria)."""

    # ... = campo obligatorio. ge=1 → el entero debe ser >= 1
    id: int = Field(..., ge=1, description="Identificador único (>= 1)")

    # str obligatorio, entre 1 y 100 caracteres
    name: str = Field(..., min_length=1, max_length=100)

    # Optional[str] = texto opcional (puede no venir; default None). Si viene, máx. 500 chars
    description: Optional[str] = Field(default=None, max_length=500)

    # Obligatorio y estrictamente mayor que 0 (gt = greater than)
    price: float = Field(..., gt=0, description="Precio debe ser > 0")

    # Si no se envía, vale False (no hace falta Field para un default simple)
    on_offer: bool = False
