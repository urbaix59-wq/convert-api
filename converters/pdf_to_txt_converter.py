from pathlib import Path
import fitz  # PyMuPDF
from .base_converter import BaseConverter


class PDFToTXTConverter(BaseConverter):
    def convert(self, input_path: Path, output_path: Path):
        doc = fitz.open(str(input_path))
        pages = [page.get_text() for page in doc]
        doc.close()

        text = "\n\n".join(pages)

        # Remplace l'extension .pdf par .txt
        txt_output = output_path.with_suffix(".txt")

        txt_output.write_text(text, encoding="utf-8", errors="ignore")
