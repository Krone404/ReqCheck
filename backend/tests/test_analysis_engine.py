from app.services.analysis_engine import AnalysisEngine
from app.preprocessing.preprocessor import PreprocessedRequirement


def test_detects_missing_shall():

    engine = AnalysisEngine()

    text = "The system processes login requests."

    result = engine.analyse(text)

    rule_ids = [f.rule_id for f in result.findings]

    assert "STR001" in rule_ids

def test_detects_missing_measurement():

    engine = AnalysisEngine()

    text = "The system shall process login requests."

    result = engine.analyse(text)

    rule_ids = [f.rule_id for f in result.findings]

    assert "TEST001" in rule_ids

def test_valid_requirement_has_fewer_findings():

    engine = AnalysisEngine()

    text = "The system shall respond within 2 seconds."

    result = engine.analyse(text)

    assert result.testability_score == 100

def test_detects_vague_term():

    engine = AnalysisEngine()

    text = "The system shall provide a fast login process."

    result = engine.analyse(text)

    rule_ids = [f.rule_id for f in result.findings]

    assert "AMB001" in rule_ids

def test_measurable_requirement_passes_testability():

    engine = AnalysisEngine()

    text = "The system shall respond within 2 seconds."

    result = engine.analyse(text)

    rule_ids = [f.rule_id for f in result.findings]

    assert "TEST001" not in rule_ids

def test_multiple_issues_detected():

    engine = AnalysisEngine()

    text = "The system may respond quickly."

    result = engine.analyse(text)

    rule_ids = [f.rule_id for f in result.findings]

    assert "AMB002" in rule_ids   # weak modal
    # STR001 is suppressed when AMB002 fires (same root cause, avoid double penalty)
    assert "STR001" not in rule_ids
    assert "TEST001" in rule_ids  # no measurable criteria

def test_preprocessor_normalizes_text():

    req = PreprocessedRequirement("The System SHALL Process Requests")

    assert req.normalized == "the system shall process requests"

def test_clarity_score_reduces_with_findings():

    engine = AnalysisEngine()

    text = "The system may respond quickly."

    result = engine.analyse(text)

    assert result.clarity_score < 100

def test_empty_requirement_scores_low():
    """An empty string should fire all structural rules, producing a low clarity score."""
    engine = AnalysisEngine()

    result = engine.analyse("")

    # STR001 and TEST001 should fire at minimum
    rule_ids = [f.rule_id for f in result.findings]
    assert "STR001" in rule_ids
    assert result.clarity_score < 100