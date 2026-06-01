from fastapi import FastAPI
from app.schemas import GateRequest #подключаемся к эндпойнту

app = FastAPI(title="VeriQA API")

@app.get("/")
def root():
    return {"message": "NurQA is running"}

@app.post("/agents/{agent_id}/gate")
def quality_gate(agent_id:str, body:GateRequest):
    return {
        "agent_id": agent_id,
        "status": "verified" if body.test_score>0.8 else "failed",
        "prompt_version": "v1.0.0",
        "checked_at": "2026-06-01"
    }

