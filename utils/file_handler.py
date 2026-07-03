import io
from docx import Document

def create_docx(text):
    doc = Document()
    doc.add_paragraph(text)
    doc_byte = io.BytesIO()
    doc.save(doc_byte)
    doc_byte.seek(0)
    return doc_byte
