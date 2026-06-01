
from typing import Optional

from pydantic import BaseModel

class GateRequest(BaseModel):
    test_score: float
    ethics_passed: bool
    prompt_version: str
    prompt_text: Optional[str] = None

class GateResponse(BaseModel):
    agent_id: str
    status: str
    tests_passed: bool
    ethics_checked: bool
