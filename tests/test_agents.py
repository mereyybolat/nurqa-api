from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_quality_gate():
    response = client.post("/agents/agent-001/gate")
    assert response.status_code == 200
    assert response.json()["agent_id"] == "agent-001"