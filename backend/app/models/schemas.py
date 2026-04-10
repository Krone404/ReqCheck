from pydantic import BaseModel, Field, field_validator
from typing import Annotated, List, Literal, Optional

class RequirementInput(BaseModel):
    text: Annotated[str, Field(min_length=1, max_length=1000)]

    @field_validator("text")
    @classmethod
    def text_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Requirement text cannot be blank")
        return v
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
    rag_error: Optional[str] = None