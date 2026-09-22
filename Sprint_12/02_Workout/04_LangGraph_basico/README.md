![Cabecera](../../../Sprint_11/assets/cabecera_thebridge.png)

# LangGraph básico (Sprint 12)

**Obligatorio** leer y ejecutar estos notebooks **después** del proyecto del agente con tools + Streamlit.

No sustituyen ese proyecto: el hito con tools sigue siendo el agente en Python. Aquí practicáis la API de LangGraph (State, nodos, edges, condicionales). La práctica evaluable con grafo llega en **Sprint 13**.

Dominio: **tarde cultural**. LLM: `langchain-google-genai` + misma `GEMINI_API_KEY`.

| Notebook | Qué aprendéis |
|----------|----------------|
| [`01_primer_grafo_langgraph.ipynb`](./01_primer_grafo_langgraph.ipynb) | StateGraph lineal: normalizar → proponer |
| [`02_condicionales_langgraph.ipynb`](./02_condicionales_langgraph.ipynb) | Conditional edges: router de intención (preferencias / eventos / horario) |

Teoría puente: [`01_Teoria/.../03_panorama_langgraph.md`](../../01_Teoria/03_Control_y_seguridad_de_tools/03_panorama_langgraph.md)  
Panorama amplio (Sprint 11): [`03_panorama_langgraph.md`](../../../Sprint_11/01_Teoria/03_Flujos_y_control_de_ejecucion/03_panorama_langgraph.md)

## Dependencias

En la primera celda de cada notebook:

```bash
%pip install -qU langgraph langchain-google-genai python-dotenv
```

## Guiones

- [`guiones_video/01_primer_grafo_langgraph.md`](./guiones_video/01_primer_grafo_langgraph.md)
- [`guiones_video/02_condicionales_langgraph.md`](./guiones_video/02_condicionales_langgraph.md)
