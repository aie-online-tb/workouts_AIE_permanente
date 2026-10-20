"""Grafo multiagente: supervisor ↔ especialistas + HITL.

Flujo:
  START → supervisor ──┬── cultura ────┐
                       ├── practico ───┼──► supervisor → …
                       └── sintetizar ─┘
                                  │
                     FINISH → aplicar (interrupt_before) → END

Stack: LangChain (ChatGoogleGenerativeAI + @tool) + LangGraph (MemorySaver).
"""

import re
from typing import Annotated, Any, Literal, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

import config
from src.llm import get_llm
from src.tools import TOOLS, ejecutar_tool


def _acumular(actual: list, nuevo: list) -> list:
    """Reducer de LangGraph: concatena listas (no pisa el valor anterior)."""
    return (actual or []) + (nuevo or [])


class EstadoGrafo(TypedDict):
    pedido: str  # mensaje del usuario
    notas_cultura: str  # las escribe el especialista cultura
    notas_practico: str  # las escribe el especialista practico
    notas_vision: str  # opcional (p. ej. cartel)
    respuesta: str  # texto del plan (sintetizar / aplicar)
    plan: list  # viñetas del plan (≥2 para HITL)
    siguiente: str  # lo elige el supervisor: cultura|practico|sintetizar|FINISH
    iteracion: int  # contador del supervisor (tope MAX_ITER)
    log: Annotated[list, _acumular]  # traza legible del orquestador
    traza_tools: Annotated[list, _acumular]  # tools usadas en los especialistas
    max_steps: int  # tope modelo↔tools dentro de un especialista
    plan_aprobado: bool  # lo escribe el humano vía update_state (HITL)
    done: bool  # True solo tras aprobar en aplicar
    pendiente_hitl: bool  # True mientras el grafo está pausado antes de aplicar


OPCIONES = ("cultura", "practico", "sintetizar", "FINISH")


def _preview(texto: str, n: int = 120) -> str:
    t = (texto or "").replace("\n", " ").strip()
    return t if len(t) <= n else t[: n - 1] + "…"


def _texto_llm(content: Any) -> str:
    """Normaliza ai.content (str o lista de bloques Gemini) a texto plano."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        partes: list[str] = []
        for bloque in content:
            if isinstance(bloque, str):
                partes.append(bloque)
            elif isinstance(bloque, dict):
                t = bloque.get("text") or bloque.get("content") or ""
                if t:
                    partes.append(str(t))
            else:
                t = getattr(bloque, "text", None)
                if t:
                    partes.append(str(t))
        return "\n".join(p.strip() for p in partes if p and str(p).strip()).strip()
    return str(content).strip()


def _parse_plan(texto: str) -> list[str]:
    items: list[str] = []
    for line in (texto or "").splitlines():
        s = line.strip()
        if s.startswith(("-", "•", "*")):
            items.append(s.lstrip("-•* ").strip())
    return [i for i in items if i]


def _ejecutar_con_tools(
    system: str,
    user: str,
    max_steps: int,
) -> tuple[str, list[dict[str, Any]]]:
    """Mini-bucle agent↔tools dentro de un especialista.

    El LLM puede pedir tools; Python las ejecuta (allowlist).
    Se repite hasta que haya texto final o se agote max_steps.
    """
    llm = get_llm().bind_tools(TOOLS)
    messages: list = [SystemMessage(content=system), HumanMessage(content=user)]
    traza: list[dict[str, Any]] = []
    texto = ""

    for paso in range(1, max(1, max_steps) + 1):
        ai: AIMessage = llm.invoke(messages)
        messages.append(ai)
        calls = getattr(ai, "tool_calls", None) or []
        if not calls:
            # Sin tool_calls → el modelo ya respondió en texto
            texto = _texto_llm(ai.content)
            break
        for call in calls:
            nombre = call.get("name") or ""
            args = dict(call.get("args") or {})
            resultado = ejecutar_tool(nombre, args)
            status = "blocked" if "no está permitida" in resultado else (
                "error" if resultado.startswith("Error") else "ok"
            )
            traza.append(
                {
                    "step": paso,
                    "tool": nombre,
                    "args": args,
                    "status": status,
                    "preview": _preview(resultado),
                }
            )
            messages.append(
                ToolMessage(content=resultado, tool_call_id=call.get("id") or nombre)
            )
    else:
        texto = texto or "He parado por max_steps en el especialista."

    return texto, traza


def _fallback_siguiente(estado: EstadoGrafo) -> str:
    """Si el LLM falla o responde mal: reglas deterministas en Python."""
    if not (estado.get("notas_cultura") or "").strip():
        return "cultura"
    if not (estado.get("notas_practico") or "").strip():
        return "practico"
    if not (estado.get("respuesta") or "").strip():
        return "sintetizar"
    return "FINISH"


def nodo_supervisor(estado: EstadoGrafo) -> dict:
    """Orquesta: no escribe el plan; solo elige el siguiente nodo (o FINISH).

    MAX_ITER evita bucles infinitos supervisor ↔ especialistas.
    """
    it = int(estado.get("iteracion") or 0) + 1
    if it >= config.MAX_ITER:
        return {
            "iteracion": it,
            "siguiente": "FINISH",
            "log": [f"iter {it}: supervisor → FINISH (MAX_ITER)"],
        }

    llm = get_llm(temperature=0)
    prompt = (
        "Eres el supervisor de un planificador cultural.\n"
        "Elige el siguiente rol:\n"
        "- cultura: ideas / encaje cultural (guía, eventos, cartel)\n"
        "- practico: logística (hora, zona, presupuesto, tiempos)\n"
        "- sintetizar: une notas en un plan final con viñetas\n"
        "- FINISH: ya hay plan/respuesta lista\n"
        "Responde SOLO una palabra: cultura, practico, sintetizar o FINISH.\n"
        "Regla: sin notas_cultura → cultura; sin notas_practico → practico; "
        "con ambas y sin respuesta → sintetizar; con respuesta → FINISH.\n\n"
        f"pedido: {estado.get('pedido')}\n"
        f"notas_cultura: {(estado.get('notas_cultura') or '')[:400]}\n"
        f"notas_practico: {(estado.get('notas_practico') or '')[:400]}\n"
        f"notas_vision: {(estado.get('notas_vision') or '')[:200]}\n"
        f"respuesta: {(estado.get('respuesta') or '')[:200]}\n"
    )
    try:
        out = llm.invoke([HumanMessage(content=prompt)])
        raw = _texto_llm(out.content)
        palabra = re.findall(r"[A-Za-z_]+", raw)
        siguiente = (palabra[0] if palabra else "").strip()
        if siguiente not in OPCIONES:
            siguiente = _fallback_siguiente(estado)
    except Exception:
        siguiente = _fallback_siguiente(estado)

    return {
        "iteracion": it,
        "siguiente": siguiente,
        "log": [f"iter {it}: supervisor → {siguiente}"],
    }


def nodo_cultura(estado: EstadoGrafo) -> dict:
    """Especialista: escribe notas_cultura (puede usar tools). No cierra el plan."""
    max_steps = int(estado.get("max_steps") or config.MAX_STEPS_DEFAULT)
    system = (
        "Eres el especialista CULTURA de una tarde en Madrid. "
        "Usa tools si ayudan (RAG_buscar_en_guia, API_consultar_eventos_madrid, "
        "describir_cartel). Si el usuario habla de cartel, entrada, poster o imagen, "
        "llama a describir_cartel (sin ruta: usa el cartel_demo del proyecto). "
        "Escribe notas cortas en español (no el plan final)."
    )
    user = (
        f"Pedido del usuario:\n{estado.get('pedido')}\n\n"
        f"Notas visión (si hay):\n{estado.get('notas_vision') or '(ninguna)'}\n\n"
        "Devuelve solo las notas culturales."
    )
    texto, traza = _ejecutar_con_tools(system, user, max_steps)
    return {
        "notas_cultura": texto,
        "traza_tools": traza,
        "log": ["cultura: notas listas"],
    }


def nodo_practico(estado: EstadoGrafo) -> dict:
    """Especialista: escribe notas_practico (logística; puede usar tools)."""
    max_steps = int(estado.get("max_steps") or config.MAX_STEPS_DEFAULT)
    system = (
        "Eres el especialista PRÁCTICO (logística). "
        "Usa tools si ayudan (hora_actual, RAG_buscar_en_guia, API…). "
        "Escribe notas cortas: zona, tiempos, presupuesto, tips. No el plan final."
    )
    user = (
        f"Pedido:\n{estado.get('pedido')}\n\n"
        f"Notas cultura:\n{estado.get('notas_cultura') or '(aún no)'}\n\n"
        "Devuelve solo las notas prácticas."
    )
    texto, traza = _ejecutar_con_tools(system, user, max_steps)
    return {
        "notas_practico": texto,
        "traza_tools": traza,
        "log": ["practico: notas listas"],
    }


def nodo_sintetizar(estado: EstadoGrafo) -> dict:
    """Une las notas en respuesta + plan (viñetas). Deja el flujo listo para HITL."""
    llm = get_llm()
    prompt = (
        "Une las notas en un plan de tarde cultural breve en español.\n"
        "Incluye al menos 2 actividades como viñetas que empiecen por '- '.\n"
        "Una intro de 1-2 frases y luego las viñetas.\n\n"
        f"Pedido: {estado.get('pedido')}\n"
        f"Cultura: {estado.get('notas_cultura')}\n"
        f"Práctico: {estado.get('notas_practico')}\n"
        f"Visión: {estado.get('notas_vision') or '(nada)'}\n"
    )
    out = llm.invoke([HumanMessage(content=prompt)])
    texto = _texto_llm(out.content)
    plan = _parse_plan(texto)
    if len(plan) < 2:
        # Fallback mínimo para poder pausar en HITL con algo que mostrar
        plan = [
            p
            for p in (
                (estado.get("notas_cultura") or "").split(".")[0].strip(),
                (estado.get("notas_practico") or "").split(".")[0].strip(),
            )
            if p
        ]
        if len(plan) < 2:
            plan = ["Actividad cultural según preferencias", "Cierre / desplazamiento"]
        texto = texto or "Plan propuesto:\n" + "\n".join(f"- {p}" for p in plan)
    return {
        "respuesta": texto,
        "plan": plan,
        "pendiente_hitl": True,
        "log": ["sintetizar: plan listo (pendiente HITL)"],
    }


def nodo_aplicar(estado: EstadoGrafo) -> dict:
    """Cierra o resetea según plan_aprobado.

    Solo se ejecuta DESPUÉS de la decisión humana: el grafo pausa con
    interrupt_before; el cliente hace update_state + invoke(None).
    """
    if estado.get("plan_aprobado"):
        prev = (estado.get("respuesta") or "").strip()
        cierre = "Plan aprobado. ¡Listo!"
        return {
            "done": True,
            "pendiente_hitl": False,
            "respuesta": f"{prev}\n\n{cierre}".strip() if prev else cierre,
            "log": ["aplicar: plan aprobado"],
        }
    return {
        "done": False,
        "pendiente_hitl": False,
        "plan_aprobado": False,
        "plan": [],
        "respuesta": (
            "Plan rechazado. Dime qué cambiar (zona, presupuesto, intereses) "
            "y proponemos otro."
        ),
        "notas_cultura": "",
        "notas_practico": "",
        "log": ["aplicar: plan rechazado"],
    }


def _router_supervisor(
    estado: EstadoGrafo,
) -> Literal["cultura", "practico", "sintetizar", "aplicar"]:
    """Lee estado['siguiente'] y elige el edge.

    FINISH → nodo aplicar (donde está el interrupt HITL).
    Si aún no hay plan/respuesta → sintetizar antes de pausar.
    """
    sig = (estado.get("siguiente") or "").strip()
    if sig == "FINISH":
        if not (estado.get("plan") or estado.get("respuesta")):
            return "sintetizar"
        return "aplicar"
    if sig in ("cultura", "practico", "sintetizar"):
        return sig  # type: ignore[return-value]
    return "sintetizar"


def build_graph():
    """Monta el grafo: especialistas vuelven al supervisor; HITL ante aplicar."""
    grafo = StateGraph(EstadoGrafo)
    grafo.add_node("supervisor", nodo_supervisor)
    grafo.add_node("cultura", nodo_cultura)
    grafo.add_node("practico", nodo_practico)
    grafo.add_node("sintetizar", nodo_sintetizar)
    grafo.add_node("aplicar", nodo_aplicar)

    grafo.add_edge(START, "supervisor")
    grafo.add_conditional_edges(
        "supervisor",
        _router_supervisor,
        {
            "cultura": "cultura",
            "practico": "practico",
            "sintetizar": "sintetizar",
            "aplicar": "aplicar",
        },
    )
    # Tras cada especialista, el control vuelve al supervisor
    grafo.add_edge("cultura", "supervisor")
    grafo.add_edge("practico", "supervisor")
    grafo.add_edge("sintetizar", "supervisor")
    grafo.add_edge("aplicar", END)

    return grafo.compile(
        checkpointer=MemorySaver(),  # checkpoints por thread_id
        interrupt_before=["aplicar"],  # pausa HITL antes de este nodo
    )


_APP = None


def get_app():
    global _APP
    if _APP is None:
        _APP = build_graph()
    return _APP


def config_hilo(thread_id: str) -> dict:
    """Config de LangGraph: identifica el hilo del checkpointer."""
    return {"configurable": {"thread_id": thread_id}}


def estado_inicial_grafo(pedido: str, max_steps: int | None = None) -> EstadoGrafo:
    return {
        "pedido": pedido,
        "notas_cultura": "",
        "notas_practico": "",
        "notas_vision": "",
        "respuesta": "",
        "plan": [],
        "siguiente": "",
        "iteracion": 0,
        "log": [],
        "traza_tools": [],
        "max_steps": max_steps if max_steps is not None else config.MAX_STEPS_DEFAULT,
        "plan_aprobado": False,
        "done": False,
        "pendiente_hitl": False,
    }


def hay_interrupt(thread_id: str) -> bool:
    """True si el hilo está pausado antes de aplicar (HITL pendiente).

    get_state(...).next incluye el nombre del siguiente nodo bloqueado.
    """
    snap = get_app().get_state(config_hilo(thread_id))
    nxt = snap.next or ()
    return "aplicar" in nxt
