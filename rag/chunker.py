from langchain_text_splitters import RecursiveCharacterTextSplitter

import os

# Convierte Docx o PDF ingresado en chunks
def splitter_docs(document, source_path):
    # Preparar Text Splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800, 
        chunk_overlap = 100
    )

    # Cortar en chunks el Docx ingresado
    docs_split = text_splitter.split_documents(document)
    
    # Bucle para asignarle una id a cada chunk(fragmento)
    for i, doc in enumerate(docs_split):
        doc.metadata["chunk_id"] = i
        doc.metadata["source"] = os.path.basename(source_path)

    return docs_split
