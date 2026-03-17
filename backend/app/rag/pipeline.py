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
    - Do NOT invent assumptions
    - Keep it simple and measurable

    Return ONLY one improved requirement.
    """

    output = generate(prompt)

    return [output]