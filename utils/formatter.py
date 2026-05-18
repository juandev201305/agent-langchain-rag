import os

# Formatea los chunks para una mayor legibilidad en el retriever
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
