from pathlib import Path
from odf.opendocument import load
from odf.text import P
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .base_converter import BaseConverter


class ODTConverter(BaseConverter):
    def convert(self, input_path: Path, output_path: Path):
        pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))

        doc = load(str(input_path))
        paragraphs = doc.getElementsByType(P)
        text = "\n".join([p.firstChild.data if p.firstChild else "" for p in paragraphs])

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
