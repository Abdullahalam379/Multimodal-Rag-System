from io import BytesIO
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@patch("app.api.routes.rag_service.index_document")
def test_index_document(mock_index):
    mock_index.return_value = {
        "status": "success",
        "document": "sample.pdf",
        "documents_extracted": 5,
        "chunks_created": 20,
        "vectors_stored": 20,
    }

    pdf = BytesIO(b"%PDF-1.4 Fake PDF")

    response = client.post(
        "/index",
        files={
            "file": (
                "sample.pdf",
                pdf,
                "application/pdf",
            )
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "success",
        "document": "sample.pdf",
        "documents_extracted": 5,
        "chunks_created": 20,
        "vectors_stored": 20,
    }

    mock_index.assert_called_once()