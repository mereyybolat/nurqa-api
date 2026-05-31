from fastapi.testclient import TestClient
from app.main import app
import pytest


@pytest.fixture
def client():
    """Creating one client for all tests"""
    with TestClient(app) as c:
        yield c