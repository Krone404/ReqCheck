import re

from app.models.schemas import Finding
from app.rules.base_rule import BaseRule
from app.preprocessing.preprocessor import PreprocessedRequirement

# Non-functional requirements should reference a recognised quality attribute
_NFR_KEYWORDS = re.compile(
    r"\b(performance|availability|reliability|security|usability|maintainability|"
    r"scalability|portability|efficiency|capacity|throughput|latency|uptime|"
    r"response\s+time|recovery|accessibility)\b"
)

# Constraint requirements should cite a specific standard, regulation, version,
# or measurable physical bound
_CONSTRAINT_SPECIFICITY = re.compile(
    r"\b(\d{1,4}[.\-]\d+|ISO|IEEE|GDPR|HIPAA|PCI|WCAG|RFC|mm|cm|kg|MHz|GHz|v\d)\b",
    re.IGNORECASE,
)

# Functional requirements should contain a recognisable system action verb
_FUNCTIONAL_VERB = re.compile(
    r"\bshall\s+(allow|enable|provide|generate|process|store|retrieve|display|send|"
    r"receive|validate|authenticate|authorise|authorize|calculate|create|update|"
    r"delete|notify|export|import|log|search|filter|sort|schedule|trigger|detect|"
    r"monitor|enforce|encrypt|decrypt|backup|restore|register|submit|upload|download|"
    r"parse|convert|format|assign|revoke|grant)\b"
)


class TypeConsistencyRule(BaseRule):
    """
    Checks that the requirement language is consistent with its declared type.

    TYPE001 — Non-functional requirement lacks a quality attribute keyword.
    TYPE002 — Constraint requirement lacks specificity (no standard, regulation, or bound).
    TYPE003 — Functional requirement lacks an identifiable system action verb.
    """

    def __init__(self, req_type: str):
        self.req_type = req_type  # "functional" | "non_functional" | "constraint"

    def apply(self, req: PreprocessedRequirement) -> list[Finding]:
        text = req.normalized

        if self.req_type == "non_functional":
            if not _NFR_KEYWORDS.search(text):
                return [Finding(
                    rule_id="TYPE001",
                    message=(
                        "This non-functional requirement does not reference a recognised "
                        "quality attribute (e.g. performance, availability, security). "
                        "Ensure the requirement describes a system quality, not a behaviour."
                    ),
                    severity="medium",
                )]

        elif self.req_type == "constraint":
            if not _CONSTRAINT_SPECIFICITY.search(text):
                return [Finding(
                    rule_id="TYPE002",
                    message=(
                        "This constraint does not reference a specific standard, regulation, "
                        "version, or measurable physical bound (e.g. GDPR Article 17, "
                        "ISO/IEC 27001:2022, 200 mm). Vague constraints cannot be verified."
                    ),
                    severity="medium",
                )]

        elif self.req_type == "functional":
            if not _FUNCTIONAL_VERB.search(text):
                return [Finding(
                    rule_id="TYPE003",
                    message=(
                        "This functional requirement does not contain a clear system action "
                        "verb (e.g. 'shall authenticate', 'shall generate', 'shall validate'). "
                        "Functional requirements must describe a specific system behaviour."
                    ),
                    severity="low",
                )]

        return []
