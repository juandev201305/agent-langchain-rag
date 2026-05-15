from docx import Document
from io import BytesIO

def generate_docx(doc_model: DocumentModel, path: str):
    doc = Document()

    # Titulo principal
    doc.add_heading(doc_model.title, level=1)

    # Secciones
    for section in doc_model.sections:
        doc.add_heading(section.title, level=2)

        for paragraph in section.paragraphs:
            doc.add_paragraph(paragraph.text)
    
    buffer = BytesIO()
    doc.save(buffer)

    buffer.seek(0)

    return buffer
