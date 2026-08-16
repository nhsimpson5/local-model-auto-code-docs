------------------------------------------------------------

extract_docstring [Function] (lines: 80-88):

Extracts a docstring from a given response string using specific markers.

Args:
    response (str): The input string containing the docstring enclosed between <<<DOCSTRING_START>>> and 
------------------------------------------------------------

generate [Function] (lines: 90-128):
Send a prompt to the local Ollama server and return the generated text.

Args:
    prompt: The full prompt to send.
    model: Ollama model tag to use. Must already be pulled locally.
    timeout: Seconds to wait before giving up (larger models are slower).
    temperature: Controls the randomness of the output. Lower values make the output more deterministic.

Raises:
    ConnectionError: if Ollama isn't reachable on localhost:11434.
    RuntimeError: if the requested model isn't available locally.
------------------------------------------------------------

build_docstring_prompt [Function] (lines: 131-149):
Build a prompt asking the model to write a docstring for one function,
in a given documentation convention (e.g. Google, NumPy, Doxygen).
------------------------------------------------------------

