from pathlib import Path
import fitz  # PyMuPDF


class ImageExtractor:
    """
    Extracts embedded images from PDF documents.
    """

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_images(self, pdf_path: str) -> list[dict]:
        """
        Extract all embedded images from a PDF.

        Args:
            pdf_path: Path to the PDF.

        Returns:
            List of metadata about extracted images.
        """

        pdf_file = Path(pdf_path)

        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        document = fitz.open(pdf_file)

        extracted_images = []

        for page_number, page in enumerate(document, start=1):

            images = page.get_images(full=True)

            for image_index, image in enumerate(images, start=1):

                xref = image[0]

                image_data = document.extract_image(xref)

                image_bytes = image_data["image"]

                extension = image_data["ext"]

                filename = (
                    f"{pdf_file.stem}"
                    f"_page_{page_number}"
                    f"_image_{image_index}.{extension}"
                )

                image_path = self.output_dir / filename

                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)

                extracted_images.append(
                    {
                        "source": pdf_file.name,
                        "page_number": page_number,
                        "image_index": image_index,
                        "image_path": str(image_path),
                    }
                )

        document.close()

        return extracted_images