import re
import json
from pathlib import Path
from app.rules.base_rule import BaseRule
from app.models.schemas import Finding
from app.preprocessing.preprocessor import PreprocessedRequirement

_DICT_PATH = Path(__file__).parent / "dictionaries" / "ambiguity_terms.json"
try:
    with open(_DICT_PATH) as _f:
        _WEAK_MODALS = json.load(_f)["weak_modals"]
except FileNotFoundError:
    raise RuntimeError(f"Ambiguity terms dictionary not found at {_DICT_PATH}")
except json.JSONDecodeError as e:
    raise RuntimeError(f"Ambiguity terms dictionary is malformed: {e}")


class ShallRule(BaseRule):

    def apply(self, req: PreprocessedRequirement):
        text = req.normalized

        if re.search(r"\bshall\b", text):
            return []

        # AMB002 already fires for weak modals at higher severity — suppress STR001
        # to avoid penalising the same root cause twice
        if any(re.search(rf"\b{m}\b", text) for m in _WEAK_MODALS):
            return []

        return [
            Finding(
                rule_id="STR001",
                message="Requirement should use 'shall' for clarity and testability.",
                severity="low"
            )
        ]