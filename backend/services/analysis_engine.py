from rules.ambiguity_rules import VagueTermRule
from rules.structure_rules import ShallRule
from models.schemas import AnalysisResult

class AnalysisEngine:

    def __init__(self):
        self.rules = [
            VagueTermRule(),
            ShallRule(),
        ]

    def analyse(self, text: str) -> AnalysisResult:
        findings = []

        for rule in self.rules:
            findings.extend(rule.apply(text))

        clarity_score = self.calculate_clarity(findings)
        testability_score = self.calculate_testability(text, findings)

        return AnalysisResult(
            findings=findings,
            clarity_score=clarity_score,
            testability_score=testability_score
        )

    def calculate_clarity(self, findings):
        penalty = sum(1 for f in findings if f.severity in ["medium", "high"])
        return max(0, 100 - penalty * 10)

    def calculate_testability(self, text, findings):
        score = 100
        if "shall" not in text.lower():
            score -= 15
        return max(0, score)