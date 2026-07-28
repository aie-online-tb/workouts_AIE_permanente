![Cabecera](../../../assets/cabecera_rag.png)

# Miniproyecto Streamlit — chat básico

Demo corta de chat (historial + streaming + sidebar mínima + tema), inspirada en [Build a basic LLM chat app](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps) para entender una web sencilla montada con Streamlit.

Sin API: la respuesta es local (plantilla + eco del mensaje). El proyecto RAG del sprint usa otra UI (pregunta → `responder()` → fuentes); aquí practicas el patrón de chat.

Antes: partes de una app mínima (`text_input` + función) en [01_streamlit.md §6](../01_streamlit.md).

---

## Paso 0 — Instalación y arranque

```bash
cd 06_miniproyecto_streamlit
python -m venv .venv
source .venv/bin/activate          # Git Bash / macOS / Linux
# .venv\Scripts\Activate.ps1       # Windows PowerShell

pip install -r requirements.txt
streamlit run app.py
```

Abre `http://localhost:8501`. Solo hace falta `app.py` (+ `requirements.txt`).

---

## Paso 1: chat + historial

Escribe varios mensajes. El hilo se guarda en `st.session_state.messages` y se vuelve a pintar en cada rerun.

En el código: `st.chat_input`, `st.chat_message` y el bucle sobre el historial.

---

## Paso 2: streaming

La respuesta del asistente aparece palabra a palabra con `st.write_stream` y un generador (`stream_palabras`). La “inteligencia” es local (frase de plantilla + eco): el objetivo es practicar la UI, no el modelo.

---

## Paso 3: sidebar mínima

En la barra lateral: cambia el **nombre del bot** (el título se actualiza) y usa **Limpiar chat** para reiniciar el hilo con un mensaje de bienvenida.

---

## Paso 4:Estilos (tema)

Los colores no van en `app.py`: están en `.streamlit/config.toml`. Al arrancar, Streamlit aplica `primaryColor`, fondos y tipografía.

Prueba a cambiar `primaryColor` (p. ej. `#0F766E` → `#B45309`), guarda y recarga la app.

Más info: [Configuration / theming](https://docs.streamlit.io/develop/concepts/configuration) en la doc oficial.

---

## Qué llevarte al proyecto RAG

| Aquí | Proyecto RAG |
|------|----------------|
| Chat multi-turno + historial | Suele bastar 1 pregunta → 1 respuesta |
| Streaming de texto | Respuesta + **fuentes** + expander debug |
| Sidebar simple | Controles opcionales (p. ej. Top-K) |

Para más patrones (feedback, LLM real…), sigue el [tutorial oficial](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps) por tu cuenta.

---

## Archivos

| Archivo | Rol |
|---------|-----|
| `app.py` | App completa |
| `.streamlit/config.toml` | Tema (colores, fuente) |
| `requirements.txt` | Streamlit |
