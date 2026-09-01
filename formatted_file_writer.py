"""
formatted_file_writer.py

writes the formatted files to the "formatted_files" folder keeping
their original names ready for replacing the originals
"""

import sys
import os

if getattr(sys, "frozen", False):
    ROOT = os.path.dirname(sys.executable)
else:
    ROOT = os.path.dirname(os.path.abspath(__file__))


def setup_formatted_folder():
    os.makedirs(os.path.join(ROOT, "formatted_files"), exist_ok=True)


def write_to_formatted_folder(file_path: str, formatted_code: str):
    with open(
        os.path.join(ROOT, "formatted_files", os.path.basename(file_path)),
        "w",
        encoding="utf-8",
        newline="",
    ) as f:
        f.write(formatted_code)
