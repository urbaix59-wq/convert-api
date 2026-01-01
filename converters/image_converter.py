from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .base_converter import BaseConverter


class ImageConverter(BaseConverter):
    def convert(self, input_path: Path, output_path: Path):
        pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))

        c = canvas.Canvas(str(output_path), pagesize=A4)
        width, height = A4

        img = ImageReader(str(input_path))
        iw, ih = img.getSize()

        scale = min(width / iw, height / ih) * 0.9
        nw, nh = iw * scale, ih * scale

        x = (width - nw) / 2
        y = (height - nh) / 2

        c.drawImage(img, x, y, nw, nh, preserveAspectRatio=True, mask="auto")
        c.showPage()
        c.save()
