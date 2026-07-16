from app.rag.chunker import Chunker
from app.rag.embedder import Embedder
from app.rag.generator import Generator
from app.rag.retriever import Retriever
from app.rag.vector_store import VectorStore
from app.services.ingestion_service import IngestionService
from pathlib import Path
from app.core.logger import logger

class RAGService:
    """
    Orchestrates the complete RAG pipeline.
    """

    def __init__(self):
        self.ingestion_service = IngestionService()
        self.chunker = Chunker()
        self.embedder = Embedder()
        self.vector_store = VectorStore()
        self.retriever = Retriever()
        self.generator = Generator()


    def index_document(self, pdf_path: str) -> dict:
        """
        Process a PDF and store it in the vector database.

        Args:
            pdf_path: Path to the PDF document.

        Returns:
            Summary of the indexing process.
        """
        logger.info(f"Indexing document: {Path(pdf_path).name}")
        documents = self.ingestion_service.ingest(pdf_path)
        logger.info(f"Ingestion produced {len(documents)} documents")

        chunks = self.chunker.chunk(documents)
        logger.info(f"Created {len(chunks)} chunks")
        embedded_chunks = self.embedder.embed(chunks)
        logger.info(f"Generated {len(embedded_chunks)} embeddings")

        self.vector_store.add_documents(embedded_chunks)
        logger.info("Indexing completed successfully")
        return {
            "status": "success",
            "document": Path(pdf_path).name,
            "documents_extracted": len(documents),
            "chunks_created": len(chunks),
            "vectors_stored": len(embedded_chunks),
        }

    def ask(self, question: str) -> str:
        """
        Answer a user's question.

        Args:
            question: User question.

        Returns:
            Generated answer.
        """
        logger.info(f"Question received: {question}")
        retrieved_chunks = self.retriever.retrieve(question)
        logger.info(f"Retrieved {len(retrieved_chunks)} chunks")

        context = self.retriever.build_context(retrieved_chunks)

        answer = self.generator.answer(question, context)
        logger.info("Answer generated successfully")
        return answer