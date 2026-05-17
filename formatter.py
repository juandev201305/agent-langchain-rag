import os

# Funcion que da un formato a los chunks para una mayor legibilidad en el retriever
def format_docs(docs):
    formatted = []

    for i, doc in enumerate(docs, 1):
        chunk_id = doc.metadata.get("chunk_id", i)
        source = doc.metadata.get("source", "desconocido")
        source = os.path.basename(source)

        page = doc.metadata.get("page", None)

        header = f"[Chunk {chunk_id}] - Fuente: {source}"
        
        if page is not None:
            header += f" - Página: {page}"

        content = doc.page_content.strip()

        formatted.append(f"{header}\n{content}")
    
    return "\n\n".join(formatted)


# Funcion para dar formatos a los resultados de distintas tools y generar un contexto final
def synthesize(web_results=None, rag_results=None):
    
    content = []

    if web_results:
        context.append("=== WEB RESULTS ===")

        for doc in web_results:
            context.append(doc["content"])
    
    if rag_results:
        context.append("\n=== RAG RESULTS ===")

        for doc in rag_results:
            content.append(doc.page_content)

    return "\n".join(context)