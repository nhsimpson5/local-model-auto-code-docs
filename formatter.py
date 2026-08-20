import subprocess


def format_file(file_path: str, language: str) -> str:
    if language == "python":
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
        result = subprocess.run(
            ["black", "-", "--quiet"],
            input=source_code,
            capture_output=True,
            text=True,
        )
    else:
        result = subprocess.run(
            ["clang-format", file_path],
            capture_output=True,
            text=True,
        )

    if result.returncode != 0:
        print(result.stderr)

    return result.stdout
