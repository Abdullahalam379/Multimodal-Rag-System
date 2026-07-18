import chromadb
from app.core.logger import logger
from app.config.settings import settings


class VectorStore:
    """
    Stores document embeddings in ChromaDB.
    """

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.vector_db_dir
        )

        self.collection = self.client.get_or_create_collection(
            name=settings.collection_name
        )

    def clear_collection(self) -> None:
        """
        Remove all vectors from the collection.
        """

        logger.info("Clearing existing vector collection")

        ids = self.collection.get()["ids"]

        if ids:
            self.collection.delete(ids=ids)

        logger.info("Vector collection cleared")

        logger.info("Vector collection cleared")

    def add_documents(self, embedded_chunks: list[dict]) -> None:
        """
        Store embedded chunks in ChromaDB.

        Args:
            embedded_chunks: Documents with embeddings.
        """

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in embedded_chunks:

            ids.append(
                f"{chunk['source']}_{chunk['chunk_id']}"
            )

            documents.append(chunk["content"])

            embeddings.append(chunk["embedding"])

            metadatas.append(
                {
                    "source": chunk["source"],
                    "page_number": chunk["page_number"],
                    "content_type": chunk["content_type"],
                    "chunk_id": chunk["chunk_id"],
                }
            )
        logger.info(f"Storing {len(ids)} vectors in ChromaDB")
        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        logger.info("Vectors stored successfully")