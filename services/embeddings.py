from langchain_openai import OpenAIEmbeddings
from config.settings import OPENROUTER_API
from config.models import EMBEDDING_MODEL

# Inicializa modelo embedding
def get_embeddings():

    return OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_base=OPENROUTER_API
    )