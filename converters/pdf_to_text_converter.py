from pathlib import Path
import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .base_converter import BaseConverter


class PDFToTextConverter(BaseConverter):
    def convert(self, input_path: Path, output_path: Path):
        pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))

        doc = fitz.open(str(input_path))
        pages = [page.get_text() for page in doc]
        doc.close()

        text = "\n\n".join(pages)

        c = canvas.Canvas(str(output_path), pagesize=letter)
        c.setFont("DejaVu", 10)

        y = 750
        for line in text.split("\n"):
            c.drawString(50, y, line[:200])
            y -= 12
            if y < 50:
                c.showPage()
                c.setFont("DejaVu", 10)
                y = 750

        c.save()
