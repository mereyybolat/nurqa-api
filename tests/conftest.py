import pytest
from app.main import app
from unittest.mock import MagicMock
import numpy as np
from fastapi.testclient import TestClient

# Mock models
mock_model = MagicMock()
mock_model.predict.return_value = np.array([1])
mock_model.predict_proba.return_value = np.array([[0.1, 0.9]])

mock_vectorizer = MagicMock()
mock_vectorizer.transform.return_value = MagicMock()

@pytest.fixture(autouse=True)
def mock_ml_models(monkeypatch):
    monkeypatch.setattr("app.model.predict.model", mock_model)
    monkeypatch.setattr("app.model.predict.vectorizer", mock_vectorizer)

@pytest.fixture
def client():
    from app.main import app
    with TestClient(app) as c:
        yield c