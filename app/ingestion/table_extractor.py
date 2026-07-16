from pathlib import Path

import pdfplumber


class TableExtractor:
    """
    Extracts tables from PDF documents.
    """

    def extract_tables(self, pdf_path: str) -> list[dict]:
        """
        Extract tables from a PDF and convert them into readable text.

        Args:
            pdf_path: Path to the PDF.

        Returns:
            List of extracted table content.
        """

        pdf_file = Path(pdf_path)

        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        extracted_tables = []

        with pdfplumber.open(pdf_file) as pdf:

            for page_number, page in enumerate(pdf.pages, start=1):

                tables = page.extract_tables()

                for table in tables:

                    if not table:
                        continue

                    headers = table[0]

                    rows = table[1:]

                    for row in rows:

                        if not row:
                            continue

                        table_text = []

                        for header, value in zip(headers, row):

                            if header and value:
                                table_text.append(
                                    f"{header.strip()}: {value.strip()}"
                                )

                        if table_text:

                            extracted_tables.append(
                                {
                                    "source": pdf_file.name,
                                    "page_number": page_number,
                                    "content_type": "table",
                                    "content": " | ".join(table_text),
                                }
                            )

        return extracted_tables