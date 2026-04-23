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

# Fire TYPE003 only when "shall" is immediately followed by a pure state verb —
# these describe what the system IS rather than what it DOES, which is a strong
# signal that a functional requirement is mis-typed or underspecified.
# Using an inverted (deny-list) approach avoids false positives on the long tail
# of valid action verbs ("support", "handle", "respond", "track", etc.).
_STATE_VERB_ONLY = re.compile(
    r"\bshall\s+(be|become|remain|stay|exist|have|contain|consist|include)\b"
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
            if _STATE_VERB_ONLY.search(text):
                return [Finding(
                    rule_id="TYPE003",
                    message=(
                        "This functional requirement uses a state verb after 'shall' "
                        "(e.g. 'shall be', 'shall remain', 'shall have'). "
                        "Functional requirements should describe a system action, not a state — "
                        "consider rewriting with an active verb (e.g. 'shall authenticate', "
                        "'shall store', 'shall respond')."
                    ),
                    severity="low",
                )]

        return []
