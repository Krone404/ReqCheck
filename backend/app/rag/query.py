import json
from pathlib import Path
from typing import List

DATA_FILE = Path(__file__).parent / "data" / "guidelines.json"

_KB: dict | None = None


def load_knowledge_base() -> dict:
    global _KB
    if _KB is not None:
        return _KB
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            _KB = json.load(file)
    except FileNotFoundError:
        raise RuntimeError(f"RAG knowledge base not found at {DATA_FILE}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"RAG knowledge base is malformed: {e}")
    return _KB


def retrieve_context(findings: List, analysis_type: str = "single_requirement") -> str:
    kb = load_knowledge_base()

    rules = kb.get("rules", [])
    usage = kb.get("usage", {})

    allowed_categories = set(usage.get(analysis_type, []))
    finding_ids = {f.rule_id for f in findings}

    matched = []
    seen = set()

    for rule in rules:
        category = rule.get("category")
        mapped = set(rule.get("mapped_rules", []))

        # Skip if wrong category
        if category not in allowed_categories:
            continue

        # Skip if no match
        if not finding_ids.intersection(mapped):
            continue

        # Avoid duplicates
        if rule["id"] in seen:
            continue

        entry = [
            f"[{rule['id']} | Section {rule['section']}]",
            f"{rule['rule']}",
            f"Guidance: {rule['guidance']}",
            f"Tip: {rule['rewrite_tip']}"
        ]

        # Add ONE example (keeps prompt clean)
        if rule.get("bad_examples"):
            entry.append(f"Bad: {rule['bad_examples'][0]}")
        if rule.get("good_examples"):
            entry.append(f"Good: {rule['good_examples'][0]}")

        matched.append("\n".join(entry))
        seen.add(rule["id"])

    if not matched:
        return "No specific ISO guidelines matched the detected issues."

    return "\n\n".join(matched)