from pathlib import Path
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .base_converter import BaseConverter


class CSVConverter(BaseConverter):
    def convert(self, input_path: Path, output_path: Path):
        pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))

        with input_path.open(encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)

        c = canvas.Canvas(str(output_path), pagesize=letter)
        c.setFont("DejaVu", 9)

        y = 750
        for row in rows:
            line = " | ".join(row)
            c.drawString(50, y, line[:200])
            y -= 12
            if y < 50:
                c.showPage()
                c.setFont("DejaVu", 9)
                y = 750

        c.save()
