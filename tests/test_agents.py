import pytest
from fastapi import status


def test_root(client):
    response = client.get("/") # отправляем GET request на root endpoint
    assert response.status_code == status.HTTP_200_OK

def test_quality_gate(client):
    response = client.post("/agents/agent-001/gate") #post request
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["agent_id"] == "agent-001" #cheking json response body

def test_quality_gate_wrong_method(client):
    #endpoint support only POST, doing reverse with GET
    response = client.get("/agents/agent-001/gate")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_quality_gate_empty_id(client):
    #empty path parameter
    response = client.post("/agents//gate")
    assert response.status_code in (status.HTTP_404_NOT_FOUND, status.HTTP_307_TEMPORARY_REDIRECT, status.HTTP_422_UNPROCESSABLE_CONTENT) # Bad Request(400) for negative, Redirect, Unprocessable Entity, зависит от фастапи маршрута


# улучшение def test_quality_gate_empty_id с помощью декоратора
@pytest.mark.parametrize("bad_path,expected_status", [
    ("/agents//gate", status.HTTP_404_NOT_FOUND),           # пустой ID
    ("/agents/ /gate", status.HTTP_200_OK),          # пробел вместо ID
    ("/agents/123/gate/", status.HTTP_200_OK),       # лишний слеш
    ("/agents/agent-id-with-💩/gate", status.HTTP_200_OK),  # эмодзи в ID
    ("/agents/../../../etc/passwd/gate", status.HTTP_404_NOT_FOUND),  # попытка взлома
])
def test_quality_gate_invalid_paths(client, bad_path, expected_status):
    response = client.post(bad_path) #using path from Parametrized test
    assert response.status_code == expected_status

def test_root_post_not_allowed(client):

    #root endpoint allows GET only
    response = client.post("/") #POST should fail at the end
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

# checking response body
def test_quality_gate_reponse_fields(client):
    
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
def test_quality_gate_exact_response(client):
    response = client.post("/agents/agent-001/gate")

    expected_response = {
        "agent_id":"agent-001",
        "status": "pending",
        "tests_passed": False,
        "ethics_checked": False
    }
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response

# Focusing on SECURITY




