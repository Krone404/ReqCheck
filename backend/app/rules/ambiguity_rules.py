import re
import json
from pathlib import Path

from app.models.schemas import Finding
from app.rules.base_rule import BaseRule
from app.preprocessing.preprocessor import PreprocessedRequirement


# Load dictionary once at startup
DICT_PATH = Path(__file__).parent / "dictionaries" / "ambiguity_terms.json"

with open(DICT_PATH) as f:
    TERMS = json.load(f)

VAGUE_TERMS = TERMS["vague_terms"]
WEAK_MODALS = TERMS["weak_modals"]
OPEN_QUANTIFIERS = TERMS["open_quantifiers"]
COMPARATIVE_TERMS = TERMS["comparatives"]

class AmbiguityRule(BaseRule):

    def apply(self, req: PreprocessedRequirement):
        findings = []
        text = req.normalized

        findings.extend(self._check_vague_terms(text))
        findings.extend(self._check_weak_modals(text))
        findings.extend(self._check_open_quantifiers(text))
        findings.extend(self._check_comparatives(text))

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
            if re.search(rf"\b{re.escape(term)}\b", text):
                findings.append(
                    Finding(
                        rule_id="AMB004",
                        message=f"Comparative term detected: '{term}' without measurable baseline.",
                        severity="medium"
                    )
                )
        return findings