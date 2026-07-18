from pydantic import BaseModel

class RetrievedChunk(BaseModel):
    """
    A single retrieved chunk used to answer the user's question.
    """

    content: str
    source: str
    page_number: int
    content_type: str
    chunk_id: int

class AskRequest(BaseModel):
    """
    Request body for asking a question.
    """

    question: str


class AskResponse(BaseModel):
    """
    Response returned after answering a question.
    """

    answer: str
    retrieved_chunks: list[RetrievedChunk]

class HealthResponse(BaseModel):
    """
    Response returned by the health endpoint.
    """

    status: str


class IndexResponse(BaseModel):
    """
    Response returned after indexing a document.
    """

    status: str
    document: str
    documents_extracted: int
    chunks_created: int
    vectors_stored: int

class SampleIndexRequest(BaseModel):
    """
    Request for indexing one of the built-in sample PDFs.
    """

    sample: str