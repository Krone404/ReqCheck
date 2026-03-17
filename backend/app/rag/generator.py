import subprocess


def generate(prompt: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=30
        )

        if result.returncode != 0:
            return "Error: LLM generation failed."

        return result.stdout.strip()

    except Exception as e:
        return f"Error: {str(e)}"