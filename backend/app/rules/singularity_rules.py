import re

from app.models.schemas import Finding
from app.rules.base_rule import BaseRule
from app.preprocessing.preprocessor import PreprocessedRequirement


# Stopwords that don't indicate a second verb clause after "and"
_STOPWORDS = {
    "a", "an", "the", "its", "their", "all", "any", "both", "each",
    "in", "on", "at", "to", "for", "of", "with", "by", "from",
}


class SingularityRule(BaseRule):

    def apply(self, req: PreprocessedRequirement):
        text = req.normalized

        # Multiple "shall" in one requirement is a clear compound obligation
        if len(re.findall(r"\bshall\b", text)) > 1:
            return [self._finding()]

        # "shall ... and <verb>" where the word after "and" is not a stopword
        # This catches: "shall backup data and notify ...", "shall log and archive ..."
        match = re.search(r"\bshall\b.+?\band\b\s+(\w+)", text)
        if match:
            word_after_and = match.group(1)
            if word_after_and not in _STOPWORDS:
                return [self._finding()]

        return []

    def _finding(self):
        return Finding(
            rule_id="SING001",
            message="Requirement may contain multiple behaviours and should be split into separate requirements.",
            severity="medium"
        )