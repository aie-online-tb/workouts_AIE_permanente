"""Tool multimodal: describe el cartel de demo (imagen → texto)."""

from pathlib import Path

from langchain_core.tools import tool

import config


@tool
def describir_cartel(ruta_imagen: str = "") -> str:
    """Describe el cartel cultural de la demo en español (hora, lugar, evento si se ven).

    Sin ruta (o cadena vacía) usa assets/cartel_demo.jpg del proyecto.
    Llama a esta tool cuando el usuario mencione cartel, entrada, poster o imagen.
    """
    path = Path(ruta_imagen) if (ruta_imagen or "").strip() else config.CARTEL_DEFAULT_PATH
    if not path.is_absolute():
        path = (config.ROOT / path).resolve()
    if not path.exists():
        return f"Error: no hay imagen en {path}"

    try:
        import os

        from google import genai
        from google.genai import types

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return "Error: falta GEMINI_API_KEY"

        mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
        client = genai.Client(api_key=api_key)
        out = client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_bytes(data=path.read_bytes(), mime_type=mime),
                        types.Part.from_text(
                            text=(
                                "Describe el cartel o entrada en 2-3 frases en español. "
                                "Si hay artista, fecha, hora o lugar, menciónalos."
                            )
                        ),
                    ],
                )
            ],
        )
        return (out.text or "").strip() or "Error: respuesta vacía del modelo."
    except Exception as e:  # noqa: BLE001
        return f"Error al leer el cartel: {e}"
