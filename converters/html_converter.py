from pathlib import Path
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .base_converter import BaseConverter


class HTMLConverter(BaseConverter):
    def convert(self, input_path: Path, output_path: Path):
        pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))

        html = input_path.read_text(encoding="utf-8", errors="ignore")

        html = re.sub(r"<(script|style).*?>.*?</\1>", "", html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub("<[^<]+?>", "", html)
        text = re.sub(r"\s+\n", "\n", text)
        text = re.sub(r"\n\s+", "\n", text)

        c = canvas.Canvas(str(output_path), pagesize=letter)
        c.setFont("DejaVu", 11)

        y = 750
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            c.drawString(50, y, line[:200])
            y -= 15
            if y < 50:
                c.showPage()
                c.setFont("DejaVu", 11)
                y = 750

        c.save()
