from pydantic import BaseModel


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