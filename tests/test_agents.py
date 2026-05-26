from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_quality_gate():
    response = client.post("/agents/agent-001/gate")
    assert response.status_code == 200
    assert response.json()["agent_id"] == "agent-001"

def test_quality_gate_wrong_method():
    response = client.get("/agents/agent-001/gate")
    assert response.status_code ==405 # Method Not Allowed


def test_quality_gate_empty_id():
    response = client.post("/agents//gate")
    assert response.status_code in (404, 307, 422) # Bad Request(400) for negative, Redirect, Unprocessable Entity, зависит от фастапи маршрута


# улучшение def test_quality_gate_empty_id с помощью декоратора
@pytest.mark.parametrize("bad_path,expected_status", [
    ("/agents//gate",404),           # пустой ID
    ("/agents/ /gate", 200),          # пробел вместо ID
    ("/agents/123/gate/", 200),       # лишний слеш
    ("/agents/agent-id-with-💩/gate", 200),  # эмодзи в ID
    ("/agents/../../../etc/passwd/gate", 404),  # попытка взлома
])
def test_quality_gate_invalid_paths(bad_path, expected_status):
    response = client.post(bad_path)
    assert response.status_code == expected_status

def test_root_post_not_allowed():
    response = client.post("/")
    assert response.status_code ==405

