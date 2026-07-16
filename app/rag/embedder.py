from openai import OpenAI
from time import perf_counter

from monitoring.metrics import EMBEDDING_TIME
from app.config.settings import settings


class Embedder:
    """
    Generates embeddings using the OpenAI Embeddings API.
    """

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

    def embed(self, chunks: list[dict]) -> list[dict]:
        """
        Generate embeddings for chunked documents.

        Args:
            chunks: Chunked documents.

        Returns:
            Chunk metadata with embeddings.
        """
        start = perf_counter()
        if not chunks:
            return []

        embedded_chunks = []

        for i in range(0, len(chunks), settings.embedding_batch_size):

            batch = chunks[i:i + settings.embedding_batch_size]

            response = self.client.embeddings.create(
                model=settings.embedding_model,
                input=[chunk["content"] for chunk in batch],
            )

            for chunk, embedding in zip(batch, response.data):

                embedded_chunks.append(
                    {
                        **chunk,
                        "embedding": embedding.embedding,
                    }
                )
        EMBEDDING_TIME.observe(
    perf_counter() - start
)
        return embedded_chunks
        