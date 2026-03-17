from app.rag.generator import generate


def rag_pipeline(text: str, findings: list):

    # Extract issues from your rule engine
    issues = "\n".join([f.message for f in findings])

    prompt = f"""
    You are improving a software requirement.

    Requirement:
    {text}

    Issues detected:
    {issues}

    Rewrite the requirement so that:
    - vague terms are removed
    - measurable criteria is included
    - use "shall"
    - make it testable

    Return ONLY the improved requirement.
    """

    output = generate(prompt)

    return [output]  # keep as list for schema