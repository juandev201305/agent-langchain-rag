from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from utils.formatter import format_docs

# Recupera documentos del retriever y construye contexto formateado
def run_pipeline_rag(query, retriever) -> str:
    try:
        docs = retriever.invoke(query)

        formatted_context = (format_docs(docs))

        return formatted_context

    except Exception as error:
        print(f"RAG error: {error}")

        return ""
