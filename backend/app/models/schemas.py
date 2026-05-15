from pydantic import BaseModel, Field, field_validator
from typing import Annotated, List, Literal, Optional

class RequirementInput(BaseModel):
    text: Annotated[str, Field(min_length=1, max_length=1000)]
    # type drives TypeConsistencyRule (TYPE001/TYPE002/TYPE003);
    # priority drives MoSCoWConsistencyRule (MOSC001/MOSC002) and the score multiplier.
    # Both default to the most common case so callers that omit them are not rejected.
    type: Literal["functional", "non_functional", "constraint"] = "functional"
    priority: Literal["must", "should", "could", "wont"] = "must"
    use_rag: bool = False

    @field_validator("text")
    @classmethod
    def text_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Requirement text cannot be blank")
        return v

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