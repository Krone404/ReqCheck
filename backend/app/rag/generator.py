import asyncio


async def generate(prompt: str) -> str:
    """Run Ollama in a subprocess without blocking the FastAPI thread pool."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "ollama", "run", "mistral",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(input=prompt.encode("utf-8")),
                timeout=30,
            )
        except asyncio.TimeoutError:
            proc.kill()
            await proc.communicate()
            return "Error: Ollama timed out after 30 seconds."

        if proc.returncode != 0:
            return f"Error: LLM generation failed. {stderr.decode('utf-8', errors='replace').strip()}"

        return stdout.decode("utf-8", errors="replace").strip()

    except FileNotFoundError:
        return "Error: ollama executable not found. Make sure Ollama is installed and on PATH."
    except Exception as e:
        return f"Error: {str(e)}"
