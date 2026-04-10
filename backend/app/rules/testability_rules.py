import re

from app.models.schemas import Finding
from app.rules.base_rule import BaseRule
from app.preprocessing.preprocessor import PreprocessedRequirement

MEASURABLE_PATTERN = (
    # Percentages: trailing \b is wrong here (% is non-word), so match separately
    r"\b\d+\.?\d*\s?%"
    r"|\b\d+\.?\d*\s?(?:seconds?|ms|milliseconds?|minutes?|hours?|days?|"
    r"users?|requests?|transactions?|mb|gb|kb|tb|rps|tps|rpm|hz)\b"
    r"|\b\d+\.?\d*-second"
)


class MeasurableCriteriaRule(BaseRule):

    def apply(self, req: PreprocessedRequirement):

        text = req.normalized

        # If measurable constraint exists, requirement is testable
        if re.search(MEASURABLE_PATTERN, text):
            return []

        return [
            Finding(
                rule_id="TEST001",
                message="Requirement lacks measurable criteria.",
                severity="low"
            )
        ]