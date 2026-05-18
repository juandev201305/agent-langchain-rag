from langchain_openai import ChatOpenAI
from config.settings import OPENROUTER_API

# Inicializa una instancia del LLM según el modelo configurado
def get_llm(model: str, temperature: float = 0):

    return ChatOpenAI(
        model=model,
        temperature=temperature,
        openai_api_base=OPENROUTER_API
    )