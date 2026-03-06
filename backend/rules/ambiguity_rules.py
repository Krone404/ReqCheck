import re
from models.schemas import Finding
from rules.base_rule import BaseRule


VAGUE_TERMS = [
    "fast", "efficient", "robust", "user-friendly",
    "quick", "simple", "intuitive", "flexible"
]

WEAK_MODALS = [
    "may", "might", "can", "could"
]

OPEN_QUANTIFIERS = [
    "etc", "and so on", "some", "many", "various"
]

COMPARATIVE_TERMS = [
    "better", "improved", "faster", "slower",
    "more efficient", "less efficient"
]


class AmbiguityRule(BaseRule):

    def apply(self, text: str):
        findings = []
        lowered = text.lower()

        findings.extend(self._check_vague_terms(lowered))
        findings.extend(self._check_weak_modals(lowered))
        findings.extend(self._check_open_quantifiers(lowered))
        findings.extend(self._check_comparatives(lowered))

        return findings


    def _check_vague_terms(self, text):
        findings = []
        for term in VAGUE_TERMS:
            if re.search(rf"\b{re.escape(term)}\b", text):
                findings.append(
                    Finding(
                        rule_id="AMB001",
                        message=f"Vague term detected: '{term}'",
                        severity="medium"
                    )
                )
        return findings


    def _check_weak_modals(self, text):
        findings = []
        for modal in WEAK_MODALS:
            if re.search(rf"\b{modal}\b", text):
                findings.append(
                    Finding(
                        rule_id="AMB002",
                        message=f"Weak modal verb detected: '{modal}'. Consider using 'shall'.",
                        severity="high"
                    )
                )
        return findings


    def _check_open_quantifiers(self, text):
        findings = []
        for term in OPEN_QUANTIFIERS:
            if re.search(rf"\b{re.escape(term)}\b", text):
                findings.append(
                    Finding(
                        rule_id="AMB003",
                        message=f"Open-ended quantifier detected: '{term}'",
                        severity="medium"
                    )
                )
        return findings


    def _check_comparatives(self, text):
        findings = []
        for term in COMPARATIVE_TERMS:
            if term in text:
                findings.append(
                    Finding(
                        rule_id="AMB004",
                        message=f"Comparative term detected: '{term}' without measurable baseline.",
                        severity="medium"
                    )
                )
        return findings