"""
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
"""

from turtle import textinput
from fastapi import FastAPI
from pydantic import BaseModel
from app.model.predict import predict

app = FastAPI(title="VeriQA is running")
class TextInput(BaseModel):
    text:str

@app.get("/")
def root():
    return {"message: VeriQA is running..."}

@app.post("/agents/{agent_id}/gate")
def quality_gate(agent_id: str):
    return{
        "agent_id":agent_id,
        "status": "verified",
        "prompt_version": "v1.0.0",
        "checked_at": "2026-06-01",
    }
@app.post("/analyze")
def analyze(input: TextInput):
    result=predict(input.text)
    return{
        "text": input.text,
        "label": result["label"],
        "confidence": result["confidence"],
        "passed_quality_gate": result["passed_quality_gate"]
    }
