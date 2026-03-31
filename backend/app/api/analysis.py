from fastapi import APIRouter, HTTPException
from app.models.schemas import RequirementInput
from app.services.analysis_engine import AnalysisEngine

router = APIRouter()
engine = AnalysisEngine()


@router.post("/analyse")
def analyse_requirement(req: RequirementInput):
    if not req.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Requirement text cannot be empty"
        )

    return engine.analyse(
        text=req.text,
        use_rag=req.use_rag
    )