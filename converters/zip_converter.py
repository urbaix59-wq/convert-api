from pathlib import Path
import zipfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .base_converter import BaseConverter


class ZIPConverter(BaseConverter):
    def convert(self, input_path: Path, output_path: Path):
        pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))

        lines = []
        with zipfile.ZipFile(str(input_path), "r") as z:
            for info in z.infolist():
                lines.append(f"{info.filename} ({info.file_size} bytes)")

        text = "\n".join(lines)

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
