from pathlib import Path

import fitz  # PyMuPDF


class PDFParser:
    """
    Responsible for extracting text from PDF documents.
    """

    def extract_text(self, pdf_path: str) -> list[dict]:
        """
        Extract text from each page of a PDF.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            A list of dictionaries containing page number and extracted text.
        """
        pdf_file = Path(pdf_path)

        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        document = fitz.open(pdf_file)

        pages = []

        for page_index, page in enumerate(document, start=1):
            pages.append(
    {
        "source": pdf_file.name,
        "page_number": page_index,
        "content_type": "text",
        "content": page.get_text().strip(),
    }
)

        document.close()

        return pages