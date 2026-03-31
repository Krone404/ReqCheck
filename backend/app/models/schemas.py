from pydantic import BaseModel
from typing import List, Literal

class RequirementInput(BaseModel):
    text: str
    type: Literal["functional", "non_functional", "constraint"]
    priority: Literal["must", "should", "could", "wont"]
    use_rag: bool = False

class Finding(BaseModel):
    rule_id: str
    message: str
    severity: Literal["low", "medium", "high"]

class AnalysisResult(BaseModel):
    findings: List[Finding]
    clarity_score: float
    testability_score: float
    suggestions: List[str] = []