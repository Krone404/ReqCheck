import re

from app.models.schemas import Finding
from app.rules.base_rule import BaseRule
from app.preprocessing.preprocessor import PreprocessedRequirement
from app.rules.ambiguity_rules import WEAK_MODALS


class MoSCoWConsistencyRule(BaseRule):
    """
    Checks that the requirement language is consistent with its MoSCoW priority.

    MOSC001 — Won't requirement uses 'shall' (mandatory language).
              Won't items must not be written as binding obligations.
    MOSC002 — Must requirement uses a weak modal instead of 'shall'.
              Must-have requirements need unambiguous mandatory language.
    """

    def __init__(self, priority: str):
        self.priority = priority  # "must" | "should" | "could" | "wont"

    def apply(self, req: PreprocessedRequirement) -> list[Finding]:
        text = req.normalized

        if self.priority == "wont":
            if re.search(r"\bshall\b", text):
                return [Finding(
                    rule_id="MOSC001",
                    message=(
                        "Won't-Have requirements must not use 'shall'. "
                        "Use 'will not' or 'is out of scope' to reflect deferred status."
                    ),
                    severity="medium",
                )]

        elif self.priority == "must":
            matched = [m for m in WEAK_MODALS if re.search(rf"\b{m}\b", text)]
            if matched:
                return [Finding(
                    rule_id="MOSC002",
                    message=(
                        f"Must-Have requirement uses weak modal(s): "
                        f"{', '.join(repr(m) for m in matched)}. "
                        "Must-Have requirements need 'shall' to express a binding obligation."
                    ),
                    severity="high",
                )]

        return []
