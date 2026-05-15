from app.rules.ambiguity_rules import AmbiguityRule
from app.rules.completeness_rules import CompletenessRule
from app.rules.moscow_rules import MoSCoWConsistencyRule
from app.rules.structure_rules import ShallRule
from app.rules.testability_rules import MeasurableCriteriaRule
from app.rules.singularity_rules import SingularityRule
from app.rules.type_rules import TypeConsistencyRule
from app.models.schemas import AnalysisResult
from app.preprocessing.preprocessor import PreprocessedRequirement
from app.rag.pipeline import rag_pipeline

# Penalty multiplier keyed by MoSCoW priority.
# Must-have items use the 1.0 baseline so scores remain on the familiar 0–100 scale.
# Lower-priority items receive reduced penalties because quality issues matter less
# for deferred or optional work.
_PRIORITY_MULTIPLIER: dict[str, float] = {
    "must":   1.0,
    "should": 0.85,
    "could":  0.70,
    "wont":   0.55,
}


class AnalysisEngine:
    def __init__(self):
        # Rules that apply regardless of priority / type
        self._base_rules = [
            AmbiguityRule(),
            CompletenessRule(),
            ShallRule(),
            MeasurableCriteriaRule(),
            SingularityRule(),
        ]

    async def analyse(
        self,
        text: str,
        use_rag: bool = False,
        priority: str = "must",
        req_type: str = "functional",
    ) -> AnalysisResult:
        req = PreprocessedRequirement(text)
        multiplier = _PRIORITY_MULTIPLIER.get(priority, 1.0)

        # Per-request rules carry request-specific state (priority, type)
        rules = self._base_rules + [
            MoSCoWConsistencyRule(priority),
            TypeConsistencyRule(req_type),
        ]

        findings = []
        for rule in rules:
            findings.extend(rule.apply(req))

        clarity_score = self.calculate_clarity(findings, multiplier)
        testability_score = self.calculate_testability(req, findings, multiplier)

        suggestions = []
        rag_error = None
        if use_rag and findings:
            suggestions, rag_error = await rag_pipeline(
                text, findings, priority, req_type
            )

        return AnalysisResult(
            findings=findings,
            clarity_score=clarity_score,
            testability_score=testability_score,
            suggestions=suggestions,
            rag_error=rag_error,
        )

    def calculate_clarity(self, findings, multiplier: float = 1.0) -> float:
        score = 100.0

        for finding in findings:
            if finding.severity == "high":
                score -= 20 * multiplier
            elif finding.severity == "medium":
                score -= 10 * multiplier
            elif finding.severity == "low":
                score -= 5 * multiplier

        return max(0.0, round(score, 1))

    def calculate_testability(self, req, findings, multiplier: float = 1.0) -> float:
        score = 100.0

        if "shall" not in req.normalized:
            score -= 15 * multiplier

        for finding in findings:
            if finding.rule_id == "TEST001":
                score -= 15 * multiplier
            elif finding.rule_id == "SING001":
                score -= 10 * multiplier
            elif finding.rule_id in ("AMB001", "AMB003", "AMB004"):
                score -= 10 * multiplier
            elif finding.rule_id == "AMB002":
                score -= 5 * multiplier

        return max(0.0, round(score, 1))
