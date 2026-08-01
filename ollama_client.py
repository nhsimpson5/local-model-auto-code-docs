"""
ollama_client.py

Thin wrapper around the local Ollama REST API for generating text completions.

Requirements before this will work:
  1. Ollama installed and running (`ollama serve`, or it runs automatically
     in the background after install on Mac/Windows).
  2. The chosen model already pulled, e.g. `ollama pull qwen2.5-coder:14b`.
"""

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen2.5-coder:14b"

def generate(prompt: str, model: str = DEFAULT_MODEL, timeout: int = 120) -> str:
    """
    Send a prompt to the local Ollama server and return the generated text.

    Args:
        prompt: The full prompt to send.
        model: Ollama model tag to use. Must already be pulled locally.
        timeout: Seconds to wait before giving up (larger models are slower).

    Raises:
        ConnectionError: if Ollama isn't reachable on localhost:11434.
        RuntimeError: if the requested model isn't available locally.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError(
            "Could not reach Ollama at localhost:11434. "
            "Is it running? Try `ollama serve` in another terminal."
        ) from e

    if response.status_code == 404:
        raise RuntimeError(
            f"Model '{model}' not found locally. Pull it first with: ollama pull {model}"
        )
    response.raise_for_status()

    return response.json()["response"].strip()


def build_docstring_prompt(name: str, source_code: str, convention: str, kind: str) -> str:
    """
    Build a prompt asking the model to write a docstring for one function,
    in a given documentation convention (e.g. Google, NumPy, Doxygen).
    """
    return (
        f"Write a {convention}-style docstring for the following {kind.lower()}. "
        "Return ONLY the docstring text itself, NO code, NO explanation, NO markdown code fences.\n\n"
        f"{kind} name: {name}\n\n"
        f"```\n{source_code}\n```"
    )
