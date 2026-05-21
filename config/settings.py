from dotenv import load_dotenv
import os
load_dotenv()

# Configuración de APIs externas

OPENROUTER_API = "https://openrouter.ai/api/v1"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

FRONTEND_URL = "*"