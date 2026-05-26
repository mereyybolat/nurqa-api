from fastapi import FastAPI

app = FastAPI(title="NurQA API")
@app.get("/")
def root():
    return {"message": "NurQA is running"}

@app.post("/agents/{agent_id}/gate")
def quality_gate(agent_id:str):
    return {
        "agent_id": agent_id,
        "status": "pending",
        "tests_passed": False,
        "ethics_checked": False
    }

