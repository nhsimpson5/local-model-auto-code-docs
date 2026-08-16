------------------------------------------------------------

CodeUnit [Class] (lines: 29-38):
One function or class found in the codebase.
------------------------------------------------------------

scan_python_file [Function] (lines: 41-86):
Extract functions/classes from a Python file using ast.
------------------------------------------------------------

scan_c_family_file [Function] (lines: 105-154):
Extract functions/classes/structs from a C or C++ file using tree-sitter.
------------------------------------------------------------

scan_codebase [Function] (lines: 157-168):
Walk a directory and extract all functions/classes from supported file types.
------------------------------------------------------------

walk [Function] (lines: 122-151):

Recursively traverses a syntax tree node and extracts code units.

Args:
    node (Tree): The current node in the syntax tree to process.

Returns:
    None: This function does not return a value. It modifies the `units` list in place.

Raises:
    None: This function does not raise any exceptions.

------------------------------------------------------------

