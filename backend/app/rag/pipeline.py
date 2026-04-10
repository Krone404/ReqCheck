from app.rag.generator import generate
from app.rag.query import retrieve_context


async def rag_pipeline(text: str, findings: list) -> tuple[list[str], str | None]:
    """Return (suggestions, error_reason). error_reason is None on success."""
    issues = "\n".join([f.message for f in findings])
    context = retrieve_context(findings, analysis_type="single_requirement")

    prompt = f"""
    You are a software requirements expert.

    Requirement:
    {text}

    Issues detected:
    {issues}

    Relevant ISO guidelines:
    {context}

    Rewrite the requirement by applying the guidance above.

    Rules:
    - Use the format: "The system shall ..."
    - Replace vague terms with measurable criteria
    - If no exact value is given, use a reasonable default (e.g. 2 seconds)
    - Keep the requirement simple, precise, and testable
    - Do NOT defer details to other documents

    Return ONLY one improved requirement.
    """

    output = await generate(prompt)

    if not output:
        return [], "AI suggestions unavailable — make sure Ollama is running locally."

    if output.startswith("Error:"):
        return [], f"AI suggestions unavailable — {output}"

    return [output.strip()], None