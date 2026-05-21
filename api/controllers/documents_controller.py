from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from services.document_service import get_documents, upload_documents, remove_document
from services.document_store import get_document

router = APIRouter()


# Obtiene documentos indexados
@router.get("/documents")
def get_all_documents():

    try:
        documents = get_documents()
        return {
            "documents": documents
        }
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Procesa e indexa documentos
@router.post("/documents/upload")
def upload_files(files: list[UploadFile] = File(...)):
    try:
        result = upload_documents(files=files)

        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Elimina documento indexado
@router.delete("/documents")
def delete_document(filename: str):
    try:
        result = remove_document(filename=filename)
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Descargar documento en memoria usando su ID y devolviéndolo como archivo descargable
@router.get("/documents/{document_id}")
def download_document(document_id: str):
    document = get_document(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    document.content.seek(0)

    return StreamingResponse(
        document.content,
        media_type=document.content_type,
        headers={
            "Content-Disposition": f'attachment; filename="{document.filename}"'
        }
    )