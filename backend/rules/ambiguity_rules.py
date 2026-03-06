import re
from models.schemas import Finding
from rules.base_rule import BaseRule

VAGUE_TERMS = [
    "fast",
    "user-friendly",
    "efficient",
    "robust",
    "quickly",
    "approximately",
    "etc"
]

class VagueTermRule(BaseRule):

    def apply(self, text: str):
        findings = []

        for term in VAGUE_TERMS:
            pattern = rf"\b{re.escape(term)}\b"
            if re.search(pattern, text, re.IGNORECASE):
                findings.append(
                    Finding(
                        rule_id="AMB001",
                        message=f"Vague term detected: '{term}'",
                        severity="medium"
                    )
                )

        return findings