"""
test_week1.py

End-to-end smoke test for week 1:
  1. Scan a folder for functions/classes/structs.
  2. Print what was found.
  3. Send them to the local LLM and print a generated docstring.

Usage:
    python test_week1.py [path_to_folder]

Defaults to ./sample_code if no path is given.
"""

import sys

from scanner import scan_codebase
from ollama_client import generate, build_docstring_prompt

_CONVENTION_BY_LANGUAGE_ = {
    "python": "Google",
    "c": "Doxygen", 
    "cpp": "Doxygen"
    }

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "sample_code"

    print(f"Scanning: {target}\n")
    units = scan_codebase(target)

    if not units:
        print(
            "No functions or classes found. Check the path, or make sure "
            "tree-sitter-languages is installed if you're scanning C/C++ files."
        )
        return

    print(f"Found {len(units)} functions/classes:\n")
    for u in units:
        doc_status = "has docstring" if u.existing_doc else "no docstring"
        print(f"  [{u.kind}] {u.name}  ({u.file_path}:{u.start_line}-{u.end_line})  [{doc_status}]")

    print(f"\n{' Generating docstrings... ':-^40}\n")
    for target_unit in units:
        prompt = build_docstring_prompt(target_unit.name, target_unit.source, target_unit.language, _CONVENTION_BY_LANGUAGE_[target_unit.language], target_unit.kind)

        try:
            result = generate(prompt)
            print(f"{target_unit.kind}: {target_unit.name}\n")
            print(result)
        except (ConnectionError, RuntimeError) as e:
            print(f"LLM call failed: {e}")
        print("\n")
        print("-"*40)
        print("\n")

    print(len("<<<DOCSTRING_START>>>"))
if __name__ == "__main__":
    main()
