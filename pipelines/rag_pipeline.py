from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from prompts import *
from formatter import format_docs

# Funcion para ejecutar RAG y obtener la respuesta del retriever(formateada)
def run_pipeline_rag(query, retriever):
    docs = retriever.invoke(query)

    context = format_docs(docs)
    
    return context
