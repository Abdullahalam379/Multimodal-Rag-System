from app.config.settings import settings
from app.ingestion.image_extractor import ImageExtractor
from app.ingestion.ocr import OCRProcessor
from app.ingestion.parser import PDFParser
from app.ingestion.table_extractor import TableExtractor
import shutil
from pathlib import Path
from app.core.logger import logger


class IngestionService:
    """
    Orchestrates the complete document ingestion pipeline.
    """
    
    def __init__(self):
        self.parser = PDFParser()
        self.image_extractor = ImageExtractor(settings.images_dir)
        self.ocr = OCRProcessor()
        self.table_extractor = TableExtractor()

    def ingest(self, pdf_path: str) -> list[dict]:
        """
        Process a PDF and return all extracted content.

        Args:
            pdf_path: Path to the PDF document.

        Returns:
            Unified list of extracted content.
        """
        logger.info(f"Starting ingestion: {Path(pdf_path).name}")
        self._clear_extracted_images()

        extracted_content = []

        # 1. Extract embedded text
        extracted_content.extend(
            self.parser.extract_text(pdf_path)
        )
        logger.info(f"Extracted {len(extracted_content)} text elements")

        # 2. Extract images
        images = self.image_extractor.extract_images(pdf_path)
        logger.info(f"Extracted {len(images)} images")
        # 3. OCR on extracted images
        extracted_content.extend(
            self.ocr.extract_text(images)
        )
        logger.info("OCR completed")

        # 4. Extract tables
        extracted_content.extend(
            self.table_extractor.extract_tables(pdf_path)
        )
        logger.info("Table extraction completed")
        
        return extracted_content
        

    def _clear_extracted_images(self) -> None:
        """
        Remove all previously extracted images.
        """

        images_dir = Path(settings.images_dir)

        if images_dir.exists():
            shutil.rmtree(images_dir)

        images_dir.mkdir(parents=True, exist_ok=True)   