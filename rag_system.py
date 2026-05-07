from config import *
from vector_store import load_vector_store
import os

# Funcion para inicializar retriever
def initialize_retriever():
    vector_store = load_vector_store()
    
    retriever = vector_store.as_retriever(
        search_type=SEARCH_TYPE,
        search_kwargs={
            "k": SEARCH_K,
            "lambda_mult": MMR_DIVERSITY_LAMBDA
        }
    )
    return retriever


