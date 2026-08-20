
"""
from fastapi.testclient import TestClient
from app.main import app
import pytest

@pytest.fixture
def client():
    ""Creating one client for all tests""
    with TestClient(app) as c:
        yield c
"""
import pytest
from unittest.mock import MagicMock, patch
import numpy as np

mock_model = MagicMock() #creating mock models
mock_model.predict.return_value = np.array([1])
mock_model.predict_proba.return_value = np.array([[0.1, 0.9]])

mock_vectorizer = MagicMock()
mock_vectorizer.transform.return_value = MagicMock()

@pytest.fixture(autouse=True)
def mock_ml_models(monkeypatch):
    monkeypatch.setattr("app.model.predict.model", mock_model)
    monkeypatch.setattr("app.model.predict.vectorizer", mock_vectorizer)
