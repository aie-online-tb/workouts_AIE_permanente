![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# Proyecto agente LangGraph · tarde cultural

El proyecto ejecutable vive en teoría (mismo patrón S11/S12):

📁 [`01_Teoria/03_Multimodal_multiagente_y_cierre/05_proyecto_agente_langgraph_tarde_cultural/`](../../01_Teoria/03_Multimodal_multiagente_y_cierre/05_proyecto_agente_langgraph_tarde_cultural/)

## Qué aporta respecto a S12

- `src/graph.py` — StateGraph agent ↔ tools (sustituye `run_tool_loop`)
- HITL — aprobar plan (`pendiente_hitl` / `plan_aprobado`) en Streamlit y CLI
- Mismo contrato `procesar_turno` + tools + `calcular_done`

## Arranque rápido

```bash
cd ../../01_Teoria/03_Multimodal_multiagente_y_cierre/05_proyecto_agente_langgraph_tarde_cultural
pip install -r requirements.txt
cp .env.example .env   # GEMINI_API_KEY
python main.py
streamlit run app.py
```
