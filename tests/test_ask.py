from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)


@patch("app.api.routes.rag_service.ask")
def test_ask(mock_ask):
    mock_ask.return_value = {
    "answer": "This is a test answer.",
    "retrieved_chunks": [],
}

    response = client.post(
        "/ask",
        json={
            "question": "What is AI?"
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["answer"] == "This is a test answer."
    assert data["retrieved_chunks"] == []