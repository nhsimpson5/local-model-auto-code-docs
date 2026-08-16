"""
main.py

Control flow:
    1. Scan a folder for functions/classes/structs.
    2. Print what was found.
    3. Send them to the local LLM.
    4. Send resulting docstrings to the doc_writer.

Usage:
    python main.py [path_to_folder]

Defaults to ./sample_code if no path is given.
"""

import sys

from scanner import scan_codebase
from ollama_client import generate, build_docstring_prompt
from doc_writer import write_to_doc, setup_docs_folder

_CONVENTION_BY_LANGUAGE_ = {
    "python": "Google",
    "c": "Doxygen", 
    "cpp": "Doxygen"
    }

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "sample_code"

    units_by_file = {}

    print(f"Scanning: {target}\n")
    units = scan_codebase(target)

    if not units:
        print(
            "No functions/classes/structs found. Check the path, or make sure "
            "tree-sitter-languages is installed if you're scanning C/C++ files."
        )
        return

    print(f"Found {len(units)} functions/classes/structs:\n")
    for u in units:
        if u.file_path not in units_by_file:
            units_by_file[u.file_path] = []
        units_by_file[u.file_path].append(u)

        doc_status = "has docstring" if u.existing_doc else "no docstring"
        print(f"  [{u.kind}] {u.name}  ({u.file_path}:{u.start_line}-{u.end_line})  [{doc_status}]")

    print(f"\n{' Generating docstrings... ':-^60}\n")
    setup_docs_folder()

    for file in units_by_file:
        unit_information = []
        for target_unit in units_by_file[file]:
            
            if target_unit.existing_doc is None:
                prompt = build_docstring_prompt(target_unit.name, target_unit.source, target_unit.language, _CONVENTION_BY_LANGUAGE_[target_unit.language], target_unit.kind)           
                try:
                    result = generate(prompt)
                except (ConnectionError, RuntimeError) as e:
                    result = f"LLM call failed: {e}"
            else:
                result = target_unit.existing_doc
            unit_information.append([target_unit.name, target_unit.kind, target_unit.start_line, target_unit.end_line, result])
        write_to_doc(file, unit_information)
            
if __name__ == "__main__":
    main()
