from langchain_community.document_loaders import Docx2txtLoader,PyPDFLoader

import os

# Carga un documento soportado
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