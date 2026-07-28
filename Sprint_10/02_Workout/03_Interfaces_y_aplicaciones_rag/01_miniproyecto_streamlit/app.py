"""Demo Streamlit — chat básico.

Inspirado en:
https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps

  1) chat + historial (session_state)
  2) streaming simulado (write_stream)
  3) sidebar: nombre del bot, bienvenida, limpiar chat
  4) tema visual (.streamlit/config.toml) pra cambiar estilos de la página

Ejecutar:

  streamlit run app.py
"""

from __future__ import annotations

import random
import time
from collections.abc import Iterator

import streamlit as st

RESPUESTAS = [
    "¡Hola! ¿En qué puedo ayudarte?",
    "Cuéntame más y te oriento.",
    "Buena pregunta. Empecemos por lo esencial.",
]


def stream_palabras(texto: str, delay: float = 0.04) -> Iterator[str]:
    for palabra in texto.split():
        yield palabra + " "
        time.sleep(delay)


def mensaje_bienvenida(nombre: str) -> dict:
    return {
        "role": "assistant",
        "content": (
            f"Hola — soy **{nombre}**. "
            "Escribe un mensaje y verás el historial y el streaming."
        ),
    }


st.set_page_config(
    page_title="Demo chat Streamlit",
    page_icon="💬",
    layout="centered",
)

# --- Nivel 3: sidebar ---
with st.sidebar:
    st.header("Configuración")
    nombre_bot = st.text_input("Nombre del bot", value="Asistente demo")
    if st.button("Limpiar chat", use_container_width=True):
        st.session_state.messages = [mensaje_bienvenida(nombre_bot)]
        st.rerun()

st.title(nombre_bot)
st.caption(
    "Demo chat con Streamlit "
    "[Tutorial oficial](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps)"
)

# --- Nivel 1: historial (+ bienvenida) ---
if "messages" not in st.session_state:
    st.session_state.messages = [mensaje_bienvenida(nombre_bot)]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Entrada + respuesta ---
if prompt := st.chat_input("Escribe un mensaje…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta local (eco + frase de plantilla); sin API
    respuesta = f"{random.choice(RESPUESTAS)}\n\n_(Eco: «{prompt}»)_"

    with st.chat_message("assistant"):
        # Nivel 2: streaming simulado
        escrito = st.write_stream(stream_palabras(respuesta))
        contenido = escrito if isinstance(escrito, str) else respuesta

    st.session_state.messages.append({"role": "assistant", "content": contenido})
