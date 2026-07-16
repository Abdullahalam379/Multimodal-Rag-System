import chromadb
from openai import OpenAI
from time import perf_counter
from monitoring.metrics import RETRIEVAL_TIME
from app.config.settings import settings


class Retriever:
    """
    Retrieves the most relevant document chunks for a user query.
    """

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

        self.chroma_client = chromadb.PersistentClient(
            path=settings.vector_db_dir
        )

        self.collection = self.chroma_client.get_or_create_collection(
            name=settings.collection_name
        )

    def retrieve(self, query: str) -> list[dict]:
        """
        Retrieve the most relevant chunks.

        Args:
            query: User question.

        Returns:
            Retrieved chunks.
        """
        start = perf_counter()
        response = self.client.embeddings.create(
            model=settings.embedding_model,
            input=query,
        )

        query_embedding = response.data[0].embedding

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=settings.top_k,
        )

        retrieved_documents = []

        for document, metadata in zip(
            results["documents"][0],
            results["metadatas"][0],
        ):
            retrieved_documents.append(
                {
                    "content": document,
                    **metadata,
                }
            )
        RETRIEVAL_TIME.observe(
    perf_counter() - start
)

        return retrieved_documents

    def build_context(self, retrieved_chunks: list[dict]) -> str:
        """
        Combine retrieved chunks into a single context string.

        Args:
            retrieved_chunks: List of retrieved document chunks.

        Returns:
            A single string with chunks separated by double newlines.
        """
        return "\n\n".join(chunk["content"] for chunk in retrieved_chunks)