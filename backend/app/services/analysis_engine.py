from app.rules.ambiguity_rules import AmbiguityRule
from app.rules.structure_rules import ShallRule
from app.rules.testability_rules import MeasurableCriteriaRule
from app.rules.singularity_rules import SingularityRule
from app.models.schemas import AnalysisResult
from app.preprocessing.preprocessor import PreprocessedRequirement
from app.rag.pipeline import rag_pipeline


class AnalysisEngine:
    def __init__(self):
        self.rules = [
            AmbiguityRule(),
            ShallRule(),
            MeasurableCriteriaRule(),
            SingularityRule()
        ]

    def analyse(self, text: str, use_rag: bool = False) -> AnalysisResult:
        req = PreprocessedRequirement(text)

        findings = []

        for rule in self.rules:
            findings.extend(rule.apply(req))

        clarity_score = self.calculate_clarity(findings)
        testability_score = self.calculate_testability(req, findings)

        suggestions = []
        rag_error = None
        if use_rag and findings:
            suggestions, rag_error = rag_pipeline(text, findings)

        return AnalysisResult(
            findings=findings,
            clarity_score=clarity_score,
            testability_score=testability_score,
            suggestions=suggestions,
            rag_error=rag_error,
        )

    def calculate_clarity(self, findings):
        score = 100

        for finding in findings:
            if finding.severity == "high":
                score -= 20
            elif finding.severity == "medium":
                score -= 10
            elif finding.severity == "low":
                score -= 5

        return max(0, score)

    def calculate_testability(self, req, findings):
        score = 100

        if "shall" not in req.normalized:
            score -= 15

        for finding in findings:
            if finding.rule_id == "TEST001":
                score -= 15
            elif finding.rule_id == "SING001":
                score -= 10

        return max(0, score)