"""
pipeline.py

Control flow:
    1. Scan a folder for functions/classes/structs.
    2. Print what was found.
    3. Send them to the local LLM.
    4. Send resulting docstrings to the doc_writer.

Usage:
    python main.py [path_to_folder]

Defaults to ./sample_code if no path is given.
"""

from scanner import scan_codebase
from ollama_client import generate, build_docstring_prompt
from doc_writer import write_to_doc, setup_docs_folder
from formatter import format_file
from formatted_file_writer import setup_formatted_folder, write_to_formatted_folder

CONVENTION_BY_LANGUAGE = {
    "python": ("Google",),
    "c": ("Doxygen",),
    "cpp": ("Doxygen",),
}


def run_pipeline(target_folder, format_check, convention_by_language):
    units_by_file = {}

    print(f"Scanning: {target_folder}\n")
    units = scan_codebase(target_folder)

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
        print(
            f"  [{u.kind}] {u.name}  ({u.file_path}:{u.start_line}-{u.end_line})  [{doc_status}]"
        )

    print(f"\n{' Generating docstrings... ':-^60}\n")
    setup_docs_folder()
    setup_formatted_folder()

    for file in units_by_file:
        unit_information = []
        for target_unit in units_by_file[file]:

            if target_unit.existing_doc is None:
                prompt = build_docstring_prompt(
                    target_unit.name,
                    target_unit.source,
                    target_unit.language,
                    convention_by_language[target_unit.language],
                    target_unit.kind,
                )
                try:
                    docstring_result = generate(prompt)
                except (ConnectionError, RuntimeError) as e:
                    docstring_result = f"LLM call failed: {e}"
            else:
                docstring_result = target_unit.existing_doc
            unit_information.append(
                [
                    target_unit.name,
                    target_unit.kind,
                    target_unit.start_line,
                    target_unit.end_line,
                    docstring_result,
                ]
            )

        write_to_doc(file, unit_information)
        if format_check:
            try:
                formatting_result = format_file(file, units_by_file[file][0].language)
                write_to_formatted_folder(file, formatting_result)
            except (FileNotFoundError, RuntimeError) as e:
                if isinstance(e, FileNotFoundError):
                    print(f"{e}: clang not installed, please install clang")
                else:
                    print(e)

    print("Done!")
