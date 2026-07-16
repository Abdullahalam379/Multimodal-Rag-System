from pathlib import Path
from app.config.settings import settings
import pytesseract
from PIL import Image
import platform
from time import perf_counter
from monitoring.metrics import OCR_TIME
# pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd
else:
    pytesseract.pytesseract.tesseract_cmd = "tesseract"


class OCRProcessor:
    """
    Extracts text from images using Tesseract OCR.
    """

    def extract_text(self, images: list[dict]) -> list[dict]:
        """
        Perform OCR on extracted images.

        Args:
            images: List of image metadata.

        Returns:
            List of OCR results.
        """
        start = perf_counter()
        ocr_results = []

        for image in images:

            image_path = Path(image["image_path"])

            if not image_path.exists():
                continue

            extracted_text = pytesseract.image_to_string(Image.open(image_path))

            extracted_text = extracted_text.strip()

            if not extracted_text:
                continue

            ocr_results.append(
                {
                    "source": image["source"],
                    "page_number": image["page_number"],
                    "content_type": "ocr",
                    "content": extracted_text,
                }
            )
        OCR_TIME.observe(
    perf_counter() - start
)
        return ocr_results