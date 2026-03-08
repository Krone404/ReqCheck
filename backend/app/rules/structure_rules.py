from app.models.schemas import Finding
from app.rules.base_rule import BaseRule
from app.preprocessing.preprocessor import PreprocessedRequirement
class ShallRule(BaseRule):

    def apply(self, req: PreprocessedRequirement):

        if "shall" not in req.normalized:
            return [
                Finding(
                    rule_id="STR001",
                    message="Requirement should use 'shall' for clarity and testability.",
                    severity="low"
                )
            ]

        return []