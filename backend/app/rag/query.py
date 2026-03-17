from typing import List

GUIDELINES = [
    "Avoid vague terms like fast, efficient, user-friendly.",
    "Requirements must be measurable and testable.",
    "Use 'shall' instead of 'should', 'may', or 'could'.",
    "Avoid open-ended terms like etc or and so on.",
    "Comparative terms require a measurable baseline."
]


def retrieve_context(findings: List) -> str:
    """
    Return relevant guidelines based on detected issues
    """

    context = []

    for f in findings:
        if f.rule_id == "AMB001":
            context.append(GUIDELINES[0])
        elif f.rule_id == "AMB002":
            context.append(GUIDELINES[2])
        elif f.rule_id == "AMB003":
            context.append(GUIDELINES[3])
        elif f.rule_id == "AMB004":
            context.append(GUIDELINES[4])
        elif f.rule_id == "TEST001":
            context.append(GUIDELINES[1])
        elif f.rule_id == "STR001":
            context.append(GUIDELINES[2])

    # remove duplicates
    return "\n".join(list(set(context)))