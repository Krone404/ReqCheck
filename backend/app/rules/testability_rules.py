import re

from app.rules.base_rule import BaseRule
from app.models.schemas import Finding
from app.preprocessing.preprocessor import PreprocessedRequirement

MEASURABLE_PATTERN = r"\b\d+\s?(seconds?|ms|milliseconds?|minutes?|hours?|users?|requests?|mb|gb|%)\b"


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