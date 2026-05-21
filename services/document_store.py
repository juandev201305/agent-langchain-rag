# almacén en memoria (se pierde al reiniciar el backend)
DOCUMENT_STORE = {}

# guarda documento usando su id como clave
def save_document(doc):
    DOCUMENT_STORE[doc.id] = doc

# obtiene documento por id
def get_document(doc_id):
    return DOCUMENT_STORE.get(doc_id)