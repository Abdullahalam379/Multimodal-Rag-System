from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)


@patch("app.api.routes.rag_service.ask")
def test_ask(mock_ask):
    mock_ask.return_value = "This is a test answer."

    response = client.post(
        "/ask",
        json={
            "question": "What is AI?"
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "This is a test answer."
    }

    mock_ask.assert_called_once_with("What is AI?")