import logging
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import RequirementInput
from app.services.analysis_engine import AnalysisEngine

logger = logging.getLogger(__name__)
router = APIRouter()


@lru_cache(maxsize=1)
def get_engine() -> AnalysisEngine:
    return AnalysisEngine()


@router.post("/analyse")
def analyse_requirement(
    req: RequirementInput,
    engine: AnalysisEngine = Depends(get_engine),
):
    try:
        return engine.analyse(text=req.text, use_rag=req.use_rag)
    except Exception:
        logger.exception("Analysis failed for requirement: %s", req.text[:80])
        raise HTTPException(status_code=500, detail="Analysis failed. Please try again.")