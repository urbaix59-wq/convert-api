from pathlib import Path
import striprtf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .base_converter import BaseConverter


class RTFConverter(BaseConverter):
    def convert(self, input_path: Path, output_path: Path):
        pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))

        text = striprtf.rtf_to_text(input_path.read_text(encoding="utf-8", errors="ignore"))

        c = canvas.Canvas(str(output_path), pagesize=letter)
        c.setFont("DejaVu", 11)

        y = 750
        for line in text.split("\n"):
            c.drawString(50, y, line)
            y -= 15
            if y < 50:
                c.showPage()
                c.setFont("DejaVu", 11)
                y = 750

        c.save()
