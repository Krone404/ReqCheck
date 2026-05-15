import re
import json
from pathlib import Path

from app.models.schemas import Finding
from app.rules.base_rule import BaseRule
from app.preprocessing.preprocessor import PreprocessedRequirement


# Load dictionary once at startup
DICT_PATH = Path(__file__).parent / "dictionaries" / "ambiguity_terms.json"

try:
    with open(DICT_PATH) as f:
        TERMS = json.load(f)
except FileNotFoundError:
    raise RuntimeError(f"Ambiguity terms dictionary not found at {DICT_PATH}")
except json.JSONDecodeError as e:
    raise RuntimeError(f"Ambiguity terms dictionary is malformed: {e}")

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
        matched = [t for t in VAGUE_TERMS if re.search(rf"\b{re.escape(t)}\b", text)]
        if not matched:
            return []
        return [Finding(
            rule_id="AMB001",
            message=f"Vague terms detected: {', '.join(repr(t) for t in matched)}. Replace with precise, measurable language.",
            severity="medium"
        )]

    def _check_weak_modals(self, text):
        matched = [m for m in WEAK_MODALS if re.search(rf"\b{m}\b", text)]
        if not matched:
            return []
        return [Finding(
            rule_id="AMB002",
            message=f"Weak modal verb(s) detected: {', '.join(repr(m) for m in matched)}. Use 'shall' for mandatory requirements.",
            severity="high"
        )]

    def _check_open_quantifiers(self, text):
        matched = [t for t in OPEN_QUANTIFIERS if re.search(rf"\b{re.escape(t)}\b", text)]
        if not matched:
            return []
        return [Finding(
            rule_id="AMB003",
            message=f"Open-ended quantifier(s) detected: {', '.join(repr(t) for t in matched)}. Specify a measurable value.",
            severity="medium"
        )]

    def _check_comparatives(self, text):
        matched = [t for t in COMPARATIVE_TERMS if re.search(rf"\b{re.escape(t)}\b", text)]
        if not matched:
            return []
        return [Finding(
            rule_id="AMB004",
            message=f"Comparative term(s) detected: {', '.join(repr(t) for t in matched)}. Provide a measurable baseline.",
            severity="medium"
        )]