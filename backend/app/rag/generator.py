import subprocess


def generate(prompt: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=30
        )

        if result.returncode != 0:
            return f"Error: LLM generation failed. {result.stderr.strip()}"

        return result.stdout.strip()

    except Exception as e:
        return f"Error: {str(e)}"