"""
run_app.py

Entry point used ONLY for building a standalone executable with PyInstaller.
You don't need this to run the app from source -- `python gui.py` (or
run.bat) is still the normal way to run it during development.

Why this file exists: a windowed (console=False) PyInstaller build sets
sys.stdout/sys.stderr to None, and pipeline.py/scanner.py/formatter.py all
call print() directly for progress and error messages. Without this guard,
the first print() call after freezing would crash with
`AttributeError: 'NoneType' object has no attribute 'write'`. Redirecting
to os.devnull turns those prints into harmless no-ops instead of a crash.

AutoCodeDocFormatting.spec currently builds with console=True, so
sys.stdout is a real console and this guard is a no-op -- but it costs
nothing to leave in, and it's what you'd need the moment you switch the
spec to console=False.
"""

import os
import sys

if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

import gui  # noqa: E402,F401  (gui.py builds and runs the window at import time)