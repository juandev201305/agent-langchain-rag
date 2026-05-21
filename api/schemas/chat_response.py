from pydantic import BaseModel

# Estructura de respuesta devuelta por el agente
class ChatResponse(BaseModel):
    response: str
    plan: dict
    document_generated: bool
    document_id: str | None = None