"""Unit tests for individual rule modules.

Each rule is tested in isolation — no engine, no preprocessing pipeline.
Tests cover at least one positive case (rule fires) and one negative case
(rule stays silent on valid input).
"""
import pytest
from app.preprocessing.preprocessor import PreprocessedRequirement
from app.rules.ambiguity_rules import AmbiguityRule
from app.rules.completeness_rules import CompletenessRule
from app.rules.singularity_rules import SingularityRule
from app.rules.structure_rules import ShallRule
from app.rules.testability_rules import MeasurableCriteriaRule


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

    def test_silent_on_protocol_list(self):
        # "TCP and UDP" are both acronym stopwords — should not fire
        findings = self._apply("The system shall support TCP and UDP.")
        assert not any(f.rule_id == "SING001" for f in findings)


# ---------------------------------------------------------------------------
# CompletenessRule (COMP001)
# ---------------------------------------------------------------------------

class TestCompletenessRule:
    rule = CompletenessRule()

    def _apply(self, text: str):
        return self.rule.apply(PreprocessedRequirement(text))

    def test_fires_on_tbd(self):
        findings = self._apply("The system shall support TBD authentication methods.")
        assert any(f.rule_id == "COMP001" for f in findings)

    def test_fires_on_etc(self):
        findings = self._apply("The system shall support PDF, CSV, etc.")
        assert any(f.rule_id == "COMP001" for f in findings)

    def test_fires_on_to_be_determined(self):
        findings = self._apply("Response time to be determined.")
        assert any(f.rule_id == "COMP001" for f in findings)

    def test_fires_on_and_so_on(self):
        findings = self._apply("The system shall handle GET, POST, and so on.")
        assert any(f.rule_id == "COMP001" for f in findings)

    def test_silent_on_complete_requirement(self):
        findings = self._apply(
            "The system shall respond within 2 seconds under 500 concurrent users."
        )
        assert not any(f.rule_id == "COMP001" for f in findings)

    def test_silent_on_as_required_by(self):
        # "as required by <named source>" is a valid specific reference, not a placeholder
        findings = self._apply(
            "The system shall encrypt data as required by GDPR Article 25."
        )
        assert not any(f.rule_id == "COMP001" for f in findings)


# ---------------------------------------------------------------------------
# TypeConsistencyRule (TYPE001 / TYPE002 / TYPE003)
# ---------------------------------------------------------------------------

from app.rules.type_rules import TypeConsistencyRule


class TestTypeConsistencyRule:
    def _apply(self, text: str, req_type: str):
        return TypeConsistencyRule(req_type).apply(PreprocessedRequirement(text))

    def test_type001_fires_on_nfr_without_quality_attribute(self):
        findings = self._apply("The system shall process login requests.", "non_functional")
        assert any(f.rule_id == "TYPE001" for f in findings)

    def test_type001_silent_on_nfr_with_quality_attribute(self):
        findings = self._apply("The system shall achieve 99.9% availability.", "non_functional")
        assert not any(f.rule_id == "TYPE001" for f in findings)

    def test_type002_fires_on_vague_constraint(self):
        findings = self._apply("The system shall comply with regulations.", "constraint")
        assert any(f.rule_id == "TYPE002" for f in findings)

    def test_type002_silent_on_specific_constraint(self):
        findings = self._apply("The system shall comply with GDPR Article 17.", "constraint")
        assert not any(f.rule_id == "TYPE002" for f in findings)

    def test_type003_fires_on_state_verb(self):
        # "shall be" is a state verb — fires TYPE003
        findings = self._apply("The system shall be available at all times.", "functional")
        assert any(f.rule_id == "TYPE003" for f in findings)

    def test_type003_fires_on_shall_remain(self):
        findings = self._apply("The system shall remain active during maintenance.", "functional")
        assert any(f.rule_id == "TYPE003" for f in findings)

    def test_type003_silent_on_action_verb(self):
        findings = self._apply(
            "The system shall authenticate users before granting access.", "functional"
        )
        assert not any(f.rule_id == "TYPE003" for f in findings)

    def test_type003_silent_on_common_unlisted_verb(self):
        # "respond", "support", "handle" are valid action verbs not in the old allowlist
        findings = self._apply("The system shall respond within 2 seconds.", "functional")
        assert not any(f.rule_id == "TYPE003" for f in findings)

    def test_no_finding_on_unknown_type(self):
        findings = self._apply("The system shall do something.", "unknown")
        assert findings == []


# ---------------------------------------------------------------------------
# MoSCoWConsistencyRule (MOSC001 / MOSC002)
# ---------------------------------------------------------------------------

from app.rules.moscow_rules import MoSCoWConsistencyRule


class TestMoSCoWConsistencyRule:
    def _apply(self, text: str, priority: str):
        return MoSCoWConsistencyRule(priority).apply(PreprocessedRequirement(text))

    def test_mosc001_fires_on_wont_with_shall(self):
        findings = self._apply("The system shall display a splash screen.", "wont")
        assert any(f.rule_id == "MOSC001" for f in findings)

    def test_mosc001_silent_on_wont_without_shall(self):
        findings = self._apply("The system will not display a splash screen.", "wont")
        assert not any(f.rule_id == "MOSC001" for f in findings)

    def test_mosc002_fires_on_must_with_weak_modal(self):
        findings = self._apply("The system may authenticate users.", "must")
        assert any(f.rule_id == "MOSC002" for f in findings)

    def test_mosc002_silent_on_must_with_shall(self):
        findings = self._apply("The system shall authenticate users.", "must")
        assert not any(f.rule_id == "MOSC002" for f in findings)

    def test_no_finding_for_should_priority(self):
        # "should" priority has no MOSC rules — neither fires
        findings = self._apply("The system may process payments.", "should")
        assert not any(f.rule_id in ("MOSC001", "MOSC002") for f in findings)

    def test_no_finding_for_could_priority(self):
        findings = self._apply("The system shall display reports.", "could")
        assert not any(f.rule_id in ("MOSC001", "MOSC002") for f in findings)
