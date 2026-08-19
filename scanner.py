"""
scanner.py

Walks a codebase and extracts functions/classes worth documenting.

  - Python files are parsed with the standard library `ast` module.
  - C/C++ files are parsed with tree-sitter, via the tree-sitter-languages
    package (prebuilt grammars, no manual compiling needed).

If tree-sitter-languages isn't installed, C/C++ scanning is silently
skipped rather than crashing, so this still runs on a Python-only repo
with zero extra setup.
"""

import ast
import os
from dataclasses import dataclass
from typing import List, Optional

try:
    from tree_sitter_language_pack import get_parser
    _TREE_SITTER_AVAILABLE = True
except ImportError:
    _TREE_SITTER_AVAILABLE = False

_IGNORED_DIR_NAMES = {".git", "__pycache__", "venv", ".venv", "node_modules", "build"}

@dataclass
class CodeUnit:
    """One function/class/struct found in the codebase."""
    name: str
    kind: str 
    file_path: str
    start_line: int
    end_line: int
    source: str
    language : str
    existing_doc: Optional[str] = None


def scan_python_file(file_path: str) -> List[CodeUnit]:
    """Extract functions/classes from a Python file using ast."""
    with open(file_path, 'r', encoding="utf-8") as f:
        source_lines = f.readlines()
    tree = ast.parse("".join(source_lines), filename=file_path)

    units = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            snippet = ""
            kind = "Function"
            start = node.lineno
            end = getattr(node, "end_lineno", start)
            snippet += "".join(source_lines[start - 1:end])
            units.append(CodeUnit(
                name=node.name,
                kind=kind,
                file_path=file_path,
                start_line=start,
                end_line=end,
                source=snippet,
                language="python",
                existing_doc=ast.get_docstring(node),
            ))
        elif isinstance(node, ast.ClassDef):
            snippet = ""
            kind = "Class"
            start = node.lineno
            end = getattr(node, "end_lineno", start)
            method_start = start
            for method in node.body:
                snippet += "".join(source_lines[method_start-1:method.lineno])
                snippet += "\t...\n"
                method_start = method.end_lineno + 1
            snippet += "".join(source_lines[method_start-1:end])
            units.append(CodeUnit(
                name=node.name,
                kind=kind,
                file_path=file_path,
                start_line=start,
                end_line=end,
                source=snippet,
                language="python",
                existing_doc=ast.get_docstring(node),
            ))
    return units


_TS_LANGUAGE_BY_EXT = {
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".hpp": "cpp",
}

_TS_UNIT_NODE_TYPES = {"function_definition", "class_specifier", "struct_specifier"}

_TS_NAME_FIELD_BY_NODE_TYPE = {
    "function_definition": "declarator",
    "class_specifier": "name",
    "struct_specifier": "name",
}

def scan_c_family_file(file_path: str) -> List[CodeUnit]:
    """Extract functions/classes/structs from a C or C++ file using tree-sitter."""
    if not _TREE_SITTER_AVAILABLE:
        return []

    ext = os.path.splitext(file_path)[1].lower()
    lang = _TS_LANGUAGE_BY_EXT.get(ext)
    if lang is None:
        return []

    parser = get_parser(lang)
    with open(file_path, "rb") as f:
        source_bytes = f.read()
    tree = parser.parse(source_bytes)

    units: List[CodeUnit] = []

    def walk(node):
        if node.type in _TS_UNIT_NODE_TYPES:
            name_node = node.child_by_field_name(_TS_NAME_FIELD_BY_NODE_TYPE[node.type]) or node
            raw_name = source_bytes[name_node.start_byte:name_node.end_byte].decode("utf-8", "ignore")
            name = raw_name.split("(")[0].strip() or "<anonymous>"
            snippet = source_bytes[node.start_byte:node.end_byte].decode("utf-8", "ignore")
            for child in node.children:
                if child.type == "field_declaration_list":
                    snippet = ""
                    cursor = node.start_byte
                    member_body_range = []
                    for member in child.children:
                        if member.type == "function_definition":
                            body_node = member.child_by_field_name("body")
                            member_body_range.append([body_node.start_byte, body_node.end_byte])
                    for body in member_body_range:
                        snippet = snippet + source_bytes[cursor :body[0]].decode("utf-8", "ignore") + "{ ... }"
                        cursor = body[1]
                    snippet = snippet + source_bytes[cursor:node.end_byte].decode("utf-8", "ignore") 
            units.append(CodeUnit(
                name=name,
                kind="Function" if node.type == "function_definition" else "Class" if node.type == "class_specifier" else "Struct",
                file_path=file_path,
                start_line=node.start_point[0] + 1,
                end_line=node.end_point[0] + 1,
                source=snippet,
                language=lang,
            ))
        for child in node.children:
            walk(child)

    walk(tree.root_node)
    return units


def scan_codebase(root_dir: str) -> List[CodeUnit]:
    """Walk a directory and extract all functions/classes/structs from supported file types."""
    all_units: List[CodeUnit] = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in _IGNORED_DIR_NAMES]
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if filename.endswith(".py"):
                all_units.extend(scan_python_file(file_path))
            elif os.path.splitext(filename)[1].lower() in _TS_LANGUAGE_BY_EXT:
                all_units.extend(scan_c_family_file(file_path))
    return all_units
