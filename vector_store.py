from langchain_chroma import Chroma 
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
from dotenv import load_dotenv
from config import *
import os
import shutil

load_dotenv()

def load_document(document):
    # Asignar la extension del documento ingreso
    extension = os.path.splitext(document)[1].lower()
    
    loaders = {
        ".docx": Docx2txtLoader,
        ".pdf": PyPDFLoader
    }

    if extension not in loaders:
        raise ValueError(f"FORMATO INCORRECTO: {extension}")
    
    # Cargar documentos ingresado
    loader = loaders[extension](document)
    return loader.load()


# Funcion para convertir el docx o pdf ingresado en chunks
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

# Funcion para inicializar vector store
def build_vector_store(docs, persist_dir="./chroma_db"):
    # Inicializar vector store
    vectorstore = Chroma.from_documents(
        docs,
        embedding=OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_base=OPENROUTER_API),
        persist_directory=persist_dir
    )
    return vectorstore
 
# Funcion para cargar vector store existente
def load_vector_store(persist_dir="./chroma_db"):
    return Chroma(
        persist_directory = persist_dir,
        embedding_function = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_base=OPENROUTER_API)
    )
 
 
 
# Funcion para resetear db chroma
def reset_chroma(persist_dir="./chroma_db"):
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)
 
# Funcion para obtener la lista de archivos almacenado en la db chroma
def get_indexed_files(vector_store):
    collection = vector_store._collection

    data = collection.get(include=["metadatas"])

    files= set()

    for metadata in data["metadatas"]:
        if "source" in metadata:
            files.add(metadata["source"])
    
    return sorted(list(files))

def delete_document(vector_store, filename):
    collection = vector_store._collection

    collection.delete(
        where={"source":filename}
    )

 