from rag.document_loader import load_document
from rag.vector_store import load_vector_store, get_indexed_files, delete_document as delete_document_from_db
from rag.chunker import splitter_docs
import os
import tempfile

# Obtiene documentos indexados
def get_documents():
    try:
        vector_store = load_vector_store()
        documents = get_indexed_files(vector_store=vector_store)
        return documents
    except Exception as e:
        RuntimeError("Error retrieving indexed documents")


# Procesa e indexa documentos en Chroma
def upload_documents(files):
    vector_store = load_vector_store()
    if not files:
        raise ValueError("No files provided")

    for file in files:
        try:
            extension = os.path.splitext(file.filename)[1]

            # Guardar archivo temporalmente para que el loader pueda leerlo
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=extension
            ) as temp_file:

                temp_file.write(file.file.read())
                temp_path = temp_file.name

            document = load_document(temp_path)

            docs_final = splitter_docs(
                document=document,
                source_path=file.filename
            )

            vector_store.add_documents(docs_final)
        except Exception as e:
            raise RuntimeError(f"Error processing "f"{file.filename}") from e
        finally:
            os.remove(temp_path)
    return {
        "uploaded_files": docs_final,
        "count": len(docs_final)
    }

# Elimina documento indexado
def remove_document(filename):
    if not filename.strip():
        raise ValueError("Filename is required")

    try:
        vector_store = load_vector_store()
        delete_document_from_db(vector_store=vector_store, filename=filename)
        return {
            "deleted": filename
        }
    except Exception as e:
        raise RuntimeError(f"Error deleting "f"{filename}") from e

