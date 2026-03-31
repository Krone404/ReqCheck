import re

from app.models.schemas import Finding
from app.rules.base_rule import BaseRule
from app.preprocessing.preprocessor import PreprocessedRequirement


MULTI_BEHAVIOUR_PATTERN = (
    r"\bshall\b.+\b(and|and/or|or)\b.+\b"
    r"(send|display|generate|log|store|encrypt|authenticate|authorise|"
    r"validate|process|record|notify|save|delete|create|update|allow|"
    r"support|return|lock|complete|handle)\b"
)


class SingularityRule(BaseRule):

    def apply(self, req: PreprocessedRequirement):
        text = req.normalized

        if re.search(MULTI_BEHAVIOUR_PATTERN, text):
            return [
                Finding(
                    rule_id="SING001",
                    message="Requirement may contain multiple behaviours and should be split into separate requirements.",
                    severity="medium"
                )
            ]

        return []