# Auto Code Documentation & Formatting

An AI-powered tool that scans a codebase, automatically generates documentation
for undocumented functions/classes, and formats code to a set of
user-selected conventions — all running **locally**, so source code never
leaves your machine.

**Status:** 🚧 In progress — Week 1 (foundational pieces: codebase scanner + local LLM hookup)

## Why local?

Uploading a private codebase to a third-party API isn't always an option.
This project uses [Ollama](https://ollama.com) to run the documentation
model entirely on your own hardware.

## Planned features

- Scan a codebase and detect undocumented functions/classes (Python, C, C++)
- Generate documentation using a local LLM, in a convention you choose
  (Google, NumPy, Doxygen, etc.)
- Auto-format code to match your preferred style (`black`, `clang-format`)
- A GUI for managing conventions and reviewing generated docs before they're
  written back to the codebase

## Tech stack

| Piece            | Tool                                   |
|-------------------|-----------------------------------------|
| Code parsing      | Python `ast` (Python), `tree-sitter` (C/C++) |
| Local inference   | [Ollama](https://ollama.com) (`qwen2.5-coder`) |
| Language(s)       | Python, with C/C++ planned              |

## Project structure

```
.
├── scanner.py          # Walks a codebase, extracts functions/classes
├── ollama_client.py    # Thin wrapper around the local Ollama REST API
├── test_week1.py        # End-to-end smoke test (scan -> generate)
├── sample_code/         # Small .py / .c files used to test the scanner
└── requirements.txt
```

## Getting started

### 1. Install and start Ollama

Download from https://ollama.com/download and install it. On Mac/Windows it
runs in the background automatically; on Linux you may need to start it
yourself:

```bash
ollama serve
```

### 2. Pull a model

```bash
ollama pull qwen2.5-coder:14b
```

On a laptop with no dedicated GPU, use a smaller model instead:

```bash
ollama pull qwen3:4b
```

If you go smaller, update `DEFAULT_MODEL` in `ollama_client.py` to match.

### 3. Set up Python

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the smoke test

```bash
python test_week1.py
```

This scans `sample_code/` (one `.py` file, one `.c` file), lists every
function/class it found, then sends each one to the local model and prints
back a generated docstring. Point it at a real folder once that works:

```bash
python test_week1.py /path/to/some/repo
```

## Troubleshooting

- **`ConnectionError: Could not reach Ollama`** — Ollama isn't running. Run `ollama serve` in another terminal.
- **`RuntimeError: Model not found`** — you haven't pulled that model yet, or the tag in `DEFAULT_MODEL` doesn't match what you pulled. Run `ollama list` to see what you have.
- **C/C++ files return 0 results** — `tree-sitter-languages` probably didn't install cleanly. Python scanning still works without it.
- **Everything is very slow** — expected for larger models on CPU-only or low-VRAM machines. Drop to a smaller model tag for development.

## Roadmap

- [x] Week 1 — codebase scanner (Python + C/C++) and local LLM hookup
- [ ] Week 2 — full pipeline: generate docs for every scanned unit, wire in the formatter (`black` / `clang-format`)
- [ ] GUI for selecting conventions and reviewing generated docs
- [ ] Custom-tuned local model

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
