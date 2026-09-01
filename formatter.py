import subprocess
import sys
import os

if getattr(sys, "frozen", False):
    BLACK_CMD = os.path.join(sys._MEIPASS, "black.exe")
    CLANG_FORMAT_CMD = os.path.join(sys._MEIPASS, "clang-format.exe")
else:
    BLACK_CMD = "black"
    CLANG_FORMAT_CMD = "clang-format"


def format_file(file_path: str, language: str) -> str:
    try:
        if language == "python":
            with open(file_path, "r", encoding="utf-8") as f:
                source_code = f.read()
            result = subprocess.run(
                ["black", "-", "--quiet"],
                input=source_code,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
        else:
            result = subprocess.run(
                ["clang-format", file_path],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
    except UnicodeDecodeError as e:
        raise e

    if result.returncode != 0:
        return result.stderr

    return result.stdout
