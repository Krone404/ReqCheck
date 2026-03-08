from rules.ambiguity_rules import AmbiguityRule
from rules.structure_rules import ShallRule
from models.schemas import AnalysisResult
from preprocessing.preprocessor import PreprocessedRequirement


class AnalysisEngine:

    def __init__(self):
        self.rules = [
            AmbiguityRule(),
            ShallRule(),
        ]

    def analyse(self, text: str) -> AnalysisResult:

        req = PreprocessedRequirement(text)

        findings = []

        for rule in self.rules:
            findings.extend(rule.apply(req))

        clarity_score = self.calculate_clarity(findings)
        testability_score = self.calculate_testability(req, findings)

        return AnalysisResult(
            findings=findings,
            clarity_score=clarity_score,
            testability_score=testability_score
        )

    def calculate_clarity(self, findings):
        penalty = sum(1 for f in findings if f.severity in ["medium", "high"])
        return max(0, 100 - penalty * 10)

    def calculate_testability(self, req, findings):

        score = 100

        if "shall" not in req.normalized:
            score -= 15

        return max(0, score)