from pydantic import BaseModel

# Estructura de datos recibida por el endpoint de chat
class ChatRequest(BaseModel):
    query: str
    model: str