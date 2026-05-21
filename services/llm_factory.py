from langchain_openai import ChatOpenAI
from config.settings import OPENROUTER_API
from config.models import GENERATION_MODEL

# Inicializa una instancia del LLM según el modelo configurado
def get_llm(model: str, temperature: float = 0):
    if not model:
        raise ValueError("Model LLM is required")
    
    valid_models = GENERATION_MODEL.values()

    if model not in valid_models:
        raise ValueError("Invalid LLM Model")
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        openai_api_base=OPENROUTER_API
    )