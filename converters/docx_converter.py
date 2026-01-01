from pathlib import Path
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .base_converter import BaseConverter


class DOCXConverter(BaseConverter):
    def convert(self, input_path: Path, output_path: Path):
        pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))

        doc = Document(str(input_path))
        paragraphs = [p.text for p in doc.paragraphs]
        text = "\n".join(paragraphs)

        c = canvas.Canvas(str(output_path), pagesize=letter)
        c.setFont("DejaVu", 12)

        y = 750
        for line in text.split("\n"):
            c.drawString(50, y, line)
            y -= 15
            if y < 50:
                c.showPage()
                c.setFont("DejaVu", 12)
                y = 750

        c.save()
