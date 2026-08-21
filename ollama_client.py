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

_EXAMPLE_BY_CONVENTION = {
    "Google": {
        "python": [
            """
def divide(a, b):
    return a / b
""",
            """
<<<DOCSTRING_START>>>
Divides one number by another.

Args:
    a (float): The dividend.
    b (float): The divisor. Must not be zero.

Returns:
    float: The result of dividing a by b.

Raises:
    ZeroDivisionError: If b is zero.
<<<DOCSTRING_END>>>
""",
        ]
    },
    "NumPy": {
        "python": [
            """
def divide(a, b):
    return a / b
""",
            """
<<<DOCSTRING_START>>>
Divides one number by another.

Parameters
----------
a : float
    The dividend.
b : float
    The divisor. Must not be zero.

Returns
-------
float
    The result of dividing a by b.

Raises
------
ZeroDivisionError
    If b is zero.
<<<DOCSTRING_END>>>
""",
        ]
    },
    "Sphinx": {
        "python": [
            """
def divide(a, b):
    return a / b
""",
            """
<<<DOCSTRING_START>>>
Divides one number by another.

:param a: The dividend.
:type a: float
:param b: The divisor. Must not be zero.
:type b: float
:returns: The result of dividing a by b.
:rtype: float
:raises ZeroDivisionError: If b is zero.
<<<DOCSTRING_END>>>
""",
        ]
    },
    "Doxygen": {
        "c": [
            """
int multiply(int a, int b) {
    return a * b;
}
""",
            """
<<<DOCSTRING_START>>>
/**
 * @brief Multiplies two integers.
 *
 * @param a The first integer factor.
 * @param b The second integer factor.
 * @return The product of a and b.
 */
<<<DOCSTRING_END>>>
""",
        ],
        "cpp": [
            """
double average(const std::vector<int>& values) {
    double sum = 0;
    for (int v : values) {
        sum += v;
    }
    return sum / values.size();
}
""",
            """
<<<DOCSTRING_START>>>
/**
 * @brief Calculates the average of a list of integers.
 *
 * @param values A vector of integers to average.
 * @return The arithmetic mean of the values. Behavior is undefined if the vector is empty.
 */
<<<DOCSTRING_END>>>
""",
        ],
    },
    "Kernel-doc": {
        "c": [
            """
int multiply(int a, int b) {
    return a * b;
}
""",
            """
<<<DOCSTRING_START>>>
/**
 * multiply() - Multiplies two integers.
 * @a: The first integer factor.
 * @b: The second integer factor.
 *
 * Return: The product of a and b.
 */
<<<DOCSTRING_END>>>
""",
        ]
    },
}


def extract_docstring(response: str) -> str:
    start = response.find("<<<DOCSTRING_START>>>")
    end = response.find("<<<DOCSTRING_END>>>")
    if start == -1 or end == -1 or end < start:
        raise RuntimeError("Model didnt follow docstring marker instructions")
    response = response[start + len("<<<DOCSTRING_START>>>") : end]
    return response


def generate(
    prompt: str,
    model: str = DEFAULT_MODEL,
    timeout: int = 120,
    temperature: float = 0.2,
) -> str:
    """
    Send a prompt to the local Ollama server and return the generated text.

    Args:
        prompt: The full prompt to send.
        model: Ollama model tag to use. Must already be pulled locally.
        timeout: Seconds to wait before giving up (larger models are slower).
        temperature: Controls the randomness of the output. Lower values make the output more deterministic.

    Raises:
        ConnectionError: if Ollama isn't reachable on localhost:11434.
        RuntimeError: if the requested model isn't available locally.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "system": "you are a precise technical documentation generator, you only output docstrings, never code or code markdown fences.",
        "stream": False,
        "options": {"temperature": temperature},
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

    return extract_docstring(response.json()["response"].strip())


def build_docstring_prompt(
    name: str, source_code: str, language: str, convention: str, kind: str
) -> str:
    """
    Build a prompt asking the model to write a docstring for one function,
    in a given documentation convention (e.g. Google, NumPy, Doxygen).
    """
    return (
        f"Write a {convention}-style docstring for the following {language} {kind.lower()} {name}.\n\n"
        "Return ONLY the docstring text itself, NO code, NO explanation, NO markdown code fences.\n\n"
        "Wrap the docstring between explicit sentinel markers, <<<DOCSTRING_START>>> and <<<DOCSTRING_END>>>, only text between these markers matters.\n\n"
        f"{kind} name: {name}\n\n"
        f"```\n{source_code}\n```\n\n"
        f"{'-'*40}\n\n"
        f"Example of a {language} {convention}-style docstring for a function:\n\n"
        f"Example {language} Function:\n\n"
        f"```\n{_EXAMPLE_BY_CONVENTION[convention][language][0]}\n```\n\n"
        f"Example Docstring:\n\n"
        f"{_EXAMPLE_BY_CONVENTION[convention][language][1]}\n\n"
        f"{'-'*40}"
    )
