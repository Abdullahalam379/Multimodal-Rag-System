from pathlib import Path
from time import perf_counter

from fastapi import APIRouter, File, HTTPException, UploadFile

from monitoring.metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    TOTAL_PIPELINE_TIME,
)

from app.api.schemas import (
    AskRequest,
    AskResponse,
    HealthResponse,
    IndexResponse,
    SampleIndexRequest
)
from app.config.settings import settings
from app.core.logger import logger
from app.services.rag_service import RAGService

router = APIRouter()

rag_service = RAGService()

@router.get("/")
def root():
    return {
        "name": "Multimodal RAG System",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
        "version": "1.0.0",
    }

@router.get(
    "/health",
    response_model=HealthResponse,
)
def health():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}


@router.post(
    "/index",
    response_model=IndexResponse,
)
async def index_document(
    file: UploadFile = File(...),
):
    """
    Upload and index a PDF document.
    """

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    REQUEST_COUNT.inc()

    start = perf_counter()

    with REQUEST_LATENCY.time():

        logger.info(f"Uploading file: {file.filename}")

        upload_dir = Path(settings.upload_dir)
        upload_dir.mkdir(parents=True, exist_ok=True)

        file_path = upload_dir / file.filename

        try:
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())

            summary = rag_service.index_document(str(file_path))

            logger.info(f"Successfully indexed: {file.filename}")

            TOTAL_PIPELINE_TIME.observe(
                perf_counter() - start
            )

            return summary

        except Exception:
            logger.exception("Indexing failed")
            raise

        finally:
            if file_path.exists():
                file_path.unlink()


@router.post(
    "/index-sample",
    response_model=IndexResponse,
)
def index_sample_document(
    request: SampleIndexRequest,
):
    """
    Index one of the built-in sample PDFs.
    """

    REQUEST_COUNT.inc()

    start = perf_counter()

    with REQUEST_LATENCY.time():

        sample_path = Path("docs") / request.sample

        if not sample_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Sample document not found.",
            )

        logger.info(f"Indexing sample document: {request.sample}")

        summary = rag_service.index_document(str(sample_path))

        logger.info(f"Successfully indexed sample: {request.sample}")

        TOTAL_PIPELINE_TIME.observe(
            perf_counter() - start
        )

        return summary


@router.post(
    "/ask",
    response_model=AskResponse,
)
def ask(
    request: AskRequest,
):
    """
    Ask a question about indexed documents.
    """

    REQUEST_COUNT.inc()

    start = perf_counter()

    with REQUEST_LATENCY.time():

        logger.info("Chat request received")

        response = rag_service.ask(request.question)

        logger.info("Chat response sent")

        TOTAL_PIPELINE_TIME.observe(
            perf_counter() - start
        )

                
        return response