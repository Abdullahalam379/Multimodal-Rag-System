from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.settings import settings


class Chunker:
    """
    Splits extracted content into overlapping chunks.
    """

    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

    def chunk(self, documents: list[dict]) -> list[dict]:
        """
        Split extracted content into chunks.

        Args:
            documents: Extracted content from the ingestion pipeline.

        Returns:
            List of chunked documents.
        """

        chunks = []
        chunk_id = 1

        for document in documents:

            split_text = self.text_splitter.split_text(
                document["content"]
            )

            for text in split_text:

                chunks.append(
                    {
                        **document,
                        "chunk_id": chunk_id,
                        "content": text,
                    }
                )

                chunk_id += 1

        return chunks