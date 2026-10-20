"""LLM LangChain (Gemini) para el grafo multiagente."""

import os

from langchain_google_genai import ChatGoogleGenerativeAI

import config
from gemini_auth import configurar_gemini_api_key


def get_llm(temperature: float | None = None) -> ChatGoogleGenerativeAI:
    configurar_gemini_api_key()
    if not os.environ.get("GEMINI_API_KEY"):
        raise RuntimeError("Falta GEMINI_API_KEY")
    return ChatGoogleGenerativeAI(
        model=config.GEMINI_MODEL,
        google_api_key=os.environ["GEMINI_API_KEY"],
        temperature=config.TEMPERATURE if temperature is None else temperature,
    )
