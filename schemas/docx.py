from pydantic import BaseModel, Field
from typing import List


class Paragraph(BaseModel):
    text: str = Field(
        description="Contenido del párrafo"
    )


class Section(BaseModel):
    title: str = Field(
        description="Título de la sección"
    )

    paragraphs: List[Paragraph] = Field(
        description="Párrafos de la sección"
    )


class DocumentModel(BaseModel):
    title: str = Field(
        description="Título principal"
    )

    objective: str = Field(
        description="Objetivo del documento"
    )

    sections: List[Section]