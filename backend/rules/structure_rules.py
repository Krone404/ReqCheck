from models.schemas import Finding
from rules.base_rule import BaseRule

class ShallRule(BaseRule):

    def apply(self, text: str):
        if "shall" not in text.lower():
            return [
                Finding(
                    rule_id="STR001",
                    message="Requirement should use 'shall' for clarity and testability.",
                    severity="low"
                )
            ]
        return []