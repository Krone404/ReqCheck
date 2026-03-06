from fastapi import APIRouter
from models.schemas import RequirementInput
from services.analysis_engine import AnalysisEngine

router = APIRouter()
engine = AnalysisEngine()

@router.post("/analyse")
def analyse_requirement(req: RequirementInput):
    return engine.analyse(req.text)