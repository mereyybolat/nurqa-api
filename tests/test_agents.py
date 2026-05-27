from fastapi.testclient import TestClient
from app.main import app
import pytest


client = TestClient(app) #создаем тестовый клиент, он имитирует HTTP requests к API

def test_root():
    response = client.get("/") # отправляем GET request на root endpoint
    assert response.status_code == 200

def test_quality_gate():
    response = client.post("/agents/agent-001/gate") #post request
    assert response.status_code == 200
    assert response.json()["agent_id"] == "agent-001" #cheking json response body

def test_quality_gate_wrong_method():
    #endpoint support only POST, doing reverse with GET
    response = client.get("/agents/agent-001/gate")
    assert response.status_code ==405 # 405=Method Not Allowed


def test_quality_gate_empty_id():
    #empty path parameter
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
    response = client.post(bad_path) #using path from Parametrized test
    assert response.status_code == expected_status

def test_root_post_not_allowed():

    #root endpoint allows GET only
    response = client.post("/") #POST should fail at the end
    assert response.status_code ==405

# checking response body
def test_quality_gate_reponse_fields():
    
    response = client.post("/agents/agent-001/gate")
    data = response.json() #saving json response to "data"
    assert response.status_code==200

    assert "agent_id" in data
    assert "status" in data
    assert "tests_passed" in data
    assert "ethics_checked" in data

    #cheking data types
    assert isinstance(data["agent_id"], str)
    assert isinstance(data["status"], str)
    assert isinstance(data["tests_passed"], bool)
    assert isinstance(data["ethics_checked"], bool)

# checking exact response: API AUTOMATION
def test_quality_gate_exact_response():
    response = client.post("/agents/agent-001/gate")

    expected_response = {
        "agent_id":"agent-001",
        "status": "pending",
        "tests_passed": False,
        "ethics_checked": False
    }
    assert response.status_code == 200
    assert response.json() == expected_response



