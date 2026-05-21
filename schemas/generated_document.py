from io import BytesIO
from dataclasses import dataclass
from datetime import datetime

# Representa un documento generado en memoria
# Incluye su contenido en BytesIO para permitir descarga/streaming
@dataclass
class GeneratedDocument:
    id: str
    content: BytesIO
    filename: str
    created_at: datetime
    content_type: str