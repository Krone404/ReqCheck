import asyncio
import logging
import re
import subprocess

logger = logging.getLogger(__name__)

# Ollama writes ANSI escape codes (spinner, progress) to stdout when it thinks
# it's attached to a terminal. Strip them from captured output.
_ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]|\x1b[()][AB012]|\x1b.")


def _run_ollama(prompt: str) -> str:
    """Synchronous subprocess call — run via run_in_executor to stay non-blocking."""
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=30,
        )

        if result.returncode != 0:
            stderr = result.stderr.strip()
            logger.error("Ollama exited %d: %s", result.returncode, stderr)
            return f"Error: LLM generation failed. {stderr}" if stderr else "Error: LLM generation failed (no stderr)."

        return _ANSI_ESCAPE.sub("", result.stdout).strip()

    except FileNotFoundError:
        logger.error("ollama executable not found")
        return "Error: ollama executable not found. Make sure Ollama is installed and on PATH."
    except subprocess.TimeoutExpired:
        logger.error("ollama timed out after 30 s")
        return "Error: Ollama timed out after 30 seconds."
    except Exception as e:
        logger.exception("Unexpected error calling ollama")
        # Include the exception type so an empty message is still informative
        msg = str(e) or "(no message)"
        return f"Error: {type(e).__name__}: {msg}"


async def generate(prompt: str) -> str:
    """Run Ollama without blocking the FastAPI event loop."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _run_ollama, prompt)
