from pathlib import Path
from PIL import Image
from fpdf import FPDF

import shutil
import fitz  # PyMuPDF


def compress_pdf(input_path, output_path):
    pdf = fitz.open(input_path)
    new_pdf = fitz.open()

    for page in pdf:
        pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
        img_bytes = pix.tobytes("jpeg")

        rect = page.rect
        new_page = new_pdf.new_page(width=rect.width, height=rect.height)
        new_page.insert_image(rect, stream=img_bytes)

    new_pdf.save(output_path)
    new_pdf.close()
    pdf.close()


def convert_file(input_path):
    input_path = Path(input_path)
    ext = input_path.suffix.lower()

    # IMAGES → PDF
    if ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"]:
        output_path = input_path.with_suffix(".pdf")
        img = Image.open(input_path).convert("RGB")
        img.save(output_path)
        return output_path

    # TXT → PDF
    if ext == ".txt":
        output_path = input_path.with_suffix(".pdf")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                pdf.multi_cell(0, 10, line)

        pdf.output(output_path)
        return output_path 
    # PDF → PDF (compression)
    if ext == ".pdf":
        converted = input_path.with_name(input_path.stem + "_converted.pdf")
        compressed = input_path.with_name(input_path.stem + "_compressed.pdf")

        shutil.copy(input_path, converted)
        compress_pdf(converted, compressed)

        return compressed

    raise ValueError(f"Format non supporté sur Render : {ext}")
