from langchain_chroma import Chroma
from services.embeddings import get_embeddings

import os
import shutil


# Inicializa vector store
def build_vector_store(
    docs,
    persist_dir="./chroma_db"
):

    return Chroma.from_documents(
        docs,
        embedding=get_embeddings(),
        persist_directory=persist_dir
    )


# Carga vector store persistida
def load_vector_store(
    persist_dir="./chroma_db"
):

    return Chroma(
        persist_directory=persist_dir,
        embedding_function=get_embeddings()
    )


# Resetea base de datos Chroma
def reset_chroma(
    persist_dir="./chroma_db"
):

    if os.path.exists(
        persist_dir
    ):
        shutil.rmtree(
            persist_dir
        )


# Obtiene documentos indexados
def get_indexed_files(
    vector_store
):

    collection = (
        vector_store._collection
    )

    data = collection.get(
        include=["metadatas"]
    )

    files = set()

    for metadata in data["metadatas"]:

        if "source" in metadata:
            files.add(
                metadata["source"]
            )

    return sorted(files)


# Elimina documento indexado
def delete_document(
    vector_store,
    filename
):

    collection = (
        vector_store._collection
    )

    collection.delete(
        where={
            "source": filename
        }
    )