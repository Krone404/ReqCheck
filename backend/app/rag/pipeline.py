from app.rag.generator import generate
from app.rag.query import retrieve_context

_PRIORITY_LABEL: dict[str, str] = {
    "must":   "Must Have — mandatory for this release",
    "should": "Should Have — high priority but not critical",
    "could":  "Could Have — nice to have if time permits",
    "wont":   "Won't Have — deferred, out of scope for this release",
}

_TYPE_LABEL: dict[str, str] = {
    "functional":     "Functional — describes a system behaviour or action",
    "non_functional": "Non-Functional — describes a system quality attribute",
    "constraint":     "Constraint — restricts design or implementation choices",
}


async def rag_pipeline(
    text: str,
    findings: list,
    priority: str = "must",
    req_type: str = "functional",
) -> tuple[list[str], str | None]:
    """Return (suggestions, error_reason). error_reason is None on success."""
    issues = "\n".join([f.message for f in findings])
    context = retrieve_context(findings, analysis_type="single_requirement")
    priority_label = _PRIORITY_LABEL.get(priority, priority)
    type_label = _TYPE_LABEL.get(req_type, req_type)

    prompt = f"""
    You are a software requirements expert.

    Requirement:
    ```
    {text}
    ```

    Requirement Type: {type_label}
    MoSCoW Priority:  {priority_label}

    Issues detected:
    {issues}

    Relevant ISO guidelines:
    {context}

    Rewrite the requirement applying the guidance above.

    Rules:
    - Use "The system shall ..." (Won't items: "The system will not ...")
    - Non-functional requirements must include a measurable quality threshold
    - Constraint requirements must cite the specific standard, clause, or bound
    - Functional requirements must name the specific system action
    - Replace vague terms with measurable criteria; use reasonable defaults if none given
    - Do NOT defer details to other documents

    Return ONLY one improved requirement.
    """

    output = await generate(prompt)

    if not output:
        return [], "AI suggestions unavailable — make sure Ollama is running locally."

    if output.startswith("Error:"):
        return [], f"AI suggestions unavailable — {output}"

    return [output.strip()], None
