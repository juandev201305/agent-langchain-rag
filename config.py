from dotenv import load_dotenv
import os
load_dotenv()


# API OPENROUTER
OPENROUTER_API = "https://openrouter.ai/api/v1"

# API KEYS
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Configuracion de modelos
EMBEDDING_MODEL = "qwen/qwen3-embedding-8b"
GENERATION_MODEL = {
    "Llama 4 Maverick (Meta)": "meta-llama/llama-4-maverick",
    "Gemini 2.5 Flash Lite (Google)": "google/gemini-2.5-flash-lite",
    "Qwen 3.5 Flash": "qwen/qwen3.5-flash-02-23",
    "Deepseek v4 pro": "deepseek/deepseek-v4-pro"
}

# CONFIGURACION DE RETRIEVER
SEARCH_TYPE = "mmr"
MMR_DIVERSITY_LAMBDA = 0.7
MMR_FETCH_K = 20
SEARCH_K = 6