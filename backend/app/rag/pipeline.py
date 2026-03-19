from app.rag.generator import generate
from app.rag.query import retrieve_context

def rag_pipeline(text: str, findings: list):

    issues = "\n".join([f.message for f in findings])

    context = retrieve_context(findings)

    prompt = f"""
    You are a software requirements expert.

    Requirement:
    {text}

    Issues detected:
    {issues}

    Relevant guidelines:
    {context}

    Rules:
    - Use the format: "The system shall ..."
    - Replace vague terms with measurable criteria
    - If no exact value is given, use a reasonable default (e.g. 2 seconds)
    - Keep the requirement simple, precise, and testable
    - Do NOT defer details to other documents

    Return ONLY one improved requirement.
    """

    output = generate(prompt)

    return [output]