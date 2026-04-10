"""Unit tests for individual rule modules.

Each rule is tested in isolation — no engine, no preprocessing pipeline.
Tests cover at least one positive case (rule fires) and one negative case
(rule stays silent on valid input).
"""
import pytest
from app.preprocessing.preprocessor import PreprocessedRequirement
from app.rules.testability_rules import MeasurableCriteriaRule
from app.rules.ambiguity_rules import AmbiguityRule
from app.rules.structure_rules import ShallRule
from app.rules.singularity_rules import SingularityRule


# ---------------------------------------------------------------------------
# MeasurableCriteriaRule (TEST001)
# ---------------------------------------------------------------------------

class TestMeasurableCriteriaRule:
    rule = MeasurableCriteriaRule()

    def _apply(self, text: str):
        return self.rule.apply(PreprocessedRequirement(text))

    def test_fires_without_measurement(self):
        findings = self._apply("The system shall process login requests.")
        assert any(f.rule_id == "TEST001" for f in findings)

    def test_silent_with_integer_unit(self):
        findings = self._apply("The system shall respond within 2 seconds.")
        assert not any(f.rule_id == "TEST001" for f in findings)

    def test_silent_with_float_unit(self):
        findings = self._apply("The system shall respond within 0.5 seconds.")
        assert not any(f.rule_id == "TEST001" for f in findings)

    def test_silent_with_percentage(self):
        findings = self._apply("The system shall achieve 99.9% uptime.")
        assert not any(f.rule_id == "TEST001" for f in findings)

    def test_silent_with_mb(self):
        findings = self._apply("The system shall support files up to 500mb.")
        assert not any(f.rule_id == "TEST001" for f in findings)

    def test_silent_with_requests(self):
        findings = self._apply("The system shall handle 1000 requests per minute.")
        assert not any(f.rule_id == "TEST001" for f in findings)


# ---------------------------------------------------------------------------
# AmbiguityRule (AMB001 / AMB002 / AMB003 / AMB004)
# ---------------------------------------------------------------------------

class TestAmbiguityRule:
    rule = AmbiguityRule()

    def _apply(self, text: str):
        return self.rule.apply(PreprocessedRequirement(text))

    def test_amb001_fires_on_vague_term(self):
        findings = self._apply("The system shall provide a fast login process.")
        assert any(f.rule_id == "AMB001" for f in findings)

    def test_amb001_single_finding_for_multiple_vague_terms(self):
        findings = self._apply(
            "The system shall provide a fast, efficient, and user-friendly login."
        )
        amb001 = [f for f in findings if f.rule_id == "AMB001"]
        assert len(amb001) == 1  # collapsed into one finding

    def test_amb001_silent_on_precise_requirement(self):
        findings = self._apply("The system shall respond within 2 seconds.")
        assert not any(f.rule_id == "AMB001" for f in findings)

    def test_amb002_fires_on_weak_modal(self):
        findings = self._apply("The system may respond to queries.")
        assert any(f.rule_id == "AMB002" for f in findings)

    def test_amb002_single_finding_for_multiple_modals(self):
        findings = self._apply("The system may or should respond to queries.")
        amb002 = [f for f in findings if f.rule_id == "AMB002"]
        assert len(amb002) == 1

    def test_amb002_silent_on_shall(self):
        findings = self._apply("The system shall respond within 2 seconds.")
        assert not any(f.rule_id == "AMB002" for f in findings)


# ---------------------------------------------------------------------------
# ShallRule (STR001)
# ---------------------------------------------------------------------------

class TestShallRule:
    rule = ShallRule()

    def _apply(self, text: str):
        return self.rule.apply(PreprocessedRequirement(text))

    def test_fires_without_shall(self):
        findings = self._apply("The system processes login requests.")
        assert any(f.rule_id == "STR001" for f in findings)

    def test_silent_with_shall(self):
        findings = self._apply("The system shall process login requests.")
        assert not any(f.rule_id == "STR001" for f in findings)

    def test_suppressed_when_weak_modal_present(self):
        # AMB002 already covers this; STR001 should not double-fire
        findings = self._apply("The system may respond to queries.")
        assert not any(f.rule_id == "STR001" for f in findings)


# ---------------------------------------------------------------------------
# SingularityRule (SING001)
# ---------------------------------------------------------------------------

class TestSingularityRule:
    rule = SingularityRule()

    def _apply(self, text: str):
        return self.rule.apply(PreprocessedRequirement(text))

    def test_fires_on_compound_requirement(self):
        findings = self._apply(
            "The system shall log all transactions and notify the administrator."
        )
        assert any(f.rule_id == "SING001" for f in findings)

    def test_fires_on_backup_and_notify(self):
        # Previously missed because "backup" wasn't in the hardcoded verb list
        findings = self._apply(
            "The system shall backup data and notify the administrator."
        )
        assert any(f.rule_id == "SING001" for f in findings)

    def test_fires_on_multiple_shall(self):
        findings = self._apply(
            "The system shall log events. The system shall archive them."
        )
        assert any(f.rule_id == "SING001" for f in findings)

    def test_silent_on_single_behaviour(self):
        findings = self._apply("The system shall log all user transactions.")
        assert not any(f.rule_id == "SING001" for f in findings)

    def test_silent_on_and_with_stopword(self):
        # "and the" should not trigger — "the" is a stopword
        findings = self._apply("The system shall store all requests and the responses.")
        assert not any(f.rule_id == "SING001" for f in findings)
