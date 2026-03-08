from app.services.analysis_engine import AnalysisEngine


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