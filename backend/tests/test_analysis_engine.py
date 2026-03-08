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
    assert "STR001" in rule_ids   # missing shall
    assert "TEST001" in rule_ids  # no measurable criteria