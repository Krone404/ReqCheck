import pytest
from app.services.analysis_engine import AnalysisEngine
from app.preprocessing.preprocessor import PreprocessedRequirement


@pytest.mark.anyio
async def test_detects_missing_shall():

    engine = AnalysisEngine()
    result = await engine.analyse("The system processes login requests.")
    rule_ids = [f.rule_id for f in result.findings]
    assert "STR001" in rule_ids


@pytest.mark.anyio
async def test_detects_missing_measurement():

    engine = AnalysisEngine()
    result = await engine.analyse("The system shall process login requests.")
    rule_ids = [f.rule_id for f in result.findings]
    assert "TEST001" in rule_ids


@pytest.mark.anyio
async def test_valid_requirement_has_fewer_findings():

    engine = AnalysisEngine()
    result = await engine.analyse("The system shall respond within 2 seconds.")
    assert result.testability_score == 100


@pytest.mark.anyio
async def test_detects_vague_term():

    engine = AnalysisEngine()
    result = await engine.analyse("The system shall provide a fast login process.")
    rule_ids = [f.rule_id for f in result.findings]
    assert "AMB001" in rule_ids


@pytest.mark.anyio
async def test_measurable_requirement_passes_testability():

    engine = AnalysisEngine()
    result = await engine.analyse("The system shall respond within 2 seconds.")
    rule_ids = [f.rule_id for f in result.findings]
    assert "TEST001" not in rule_ids


@pytest.mark.anyio
async def test_multiple_issues_detected():

    engine = AnalysisEngine()
    result = await engine.analyse("The system may respond quickly.")
    rule_ids = [f.rule_id for f in result.findings]
    assert "AMB002" in rule_ids   # weak modal
    # STR001 is suppressed when AMB002 fires (same root cause, avoid double penalty)
    assert "STR001" not in rule_ids
    assert "TEST001" in rule_ids  # no measurable criteria


def test_preprocessor_normalizes_text():

    req = PreprocessedRequirement("The System SHALL Process Requests")
    assert req.normalized == "the system shall process requests"


@pytest.mark.anyio
async def test_clarity_score_reduces_with_findings():

    engine = AnalysisEngine()
    result = await engine.analyse("The system may respond quickly.")
    assert result.clarity_score < 100


@pytest.mark.anyio
async def test_empty_requirement_scores_low():
    """An empty string should fire all structural rules, producing a low clarity score."""
    engine = AnalysisEngine()
    result = await engine.analyse("")
    rule_ids = [f.rule_id for f in result.findings]
    assert "STR001" in rule_ids
    assert result.clarity_score < 100
