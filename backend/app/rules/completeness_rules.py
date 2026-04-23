import re

from app.models.schemas import Finding
from app.rules.base_rule import BaseRule
from app.preprocessing.preprocessor import PreprocessedRequirement

# Phrases that signal an incomplete or deferred requirement (ISO 29148 §5.2.5)
_INCOMPLETE_PATTERNS = [
    r"\bTBD\b",
    r"\bTBS\b",
    r"\bTBR\b",
    r"\bto\s+be\s+determined\b",
    r"\bto\s+be\s+specified\b",
    r"\bto\s+be\s+resolved\b",
    r"\bsee\s+above\b",
    r"\bas\s+needed\b",
    r"\bas\s+required\b",
    r"\bdetails\s+to\s+follow\b",
    r"\betc\.?\b",
    r"\band\s+so\s+on\b",
]

_COMPILED = [re.compile(p, re.IGNORECASE) for p in _INCOMPLETE_PATTERNS]


class CompletenessRule(BaseRule):

    def apply(self, req: PreprocessedRequirement):
        text = req.original

        matched = [p.pattern for p in _COMPILED if p.search(text)]
        if not matched:
            return []

        return [
            Finding(
                rule_id="COMP001",
                message=(
                    "Requirement appears incomplete — contains deferred or open-ended "
                    "placeholder language. Resolve all TBD/TBS/TBR items and replace "
                    "open-ended phrases with specific, measurable criteria."
                ),
                severity="high",
            )
        ]
