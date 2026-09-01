# AutoCodeDocFormatting.spec
#
# PyInstaller spec for building a standalone Windows executable.
# Build with:
#
#     pyinstaller AutoCodeDocFormatting.spec
#
# See BUILD.md for the full walkthrough and troubleshooting if the build
# fails or the .exe crashes on startup.

import os
import sys

from PyInstaller.utils.hooks import collect_all

block_cipher = None

datas = []
binaries = []
hiddenimports = []

# tree-sitter-language-pack ships its C/C++ grammar bindings as compiled
# package data, not as pure Python -- PyInstaller's static import analysis
# can't see those on its own, so collect_all() pulls in the data files,
# compiled extensions, and submodules explicitly. Without this, the built
# .exe runs but silently returns 0 results for every C/C++ file.
for pkg in ("tree_sitter_language_pack", "tree_sitter"):
    _datas, _binaries, _hiddenimports = collect_all(pkg)
    datas += _datas
    binaries += _binaries
    hiddenimports += _hiddenimports

# formatter.py shells out to "black" and "clang-format" as external
# commands. pip drops launcher .exes for both into the active venv's
# Scripts\ folder, which is only on PATH while the venv is active -- a
# frozen build has neither, so we bundle the two .exes directly here and
# formatter.py looks them up at runtime via sys._MEIPASS (see the
# sys.frozen check that needs adding there -- BUILD.md has the details).
_scripts_dir = os.path.join(sys.prefix, "Scripts")
for _exe_name in ("black.exe", "clang-format.exe"):
    _exe_path = os.path.join(_scripts_dir, _exe_name)
    if os.path.exists(_exe_path):
        binaries.append((_exe_path, "."))
    else:
        print(f"WARNING: {_exe_path} not found -- run `pip install black clang-format` "
              f"in this venv before building, or formatting will fail in the built exe.")

a = Analysis(
    ["run_app.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="AutoCodeDocFormatting",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # keep the console window visible for now -- see BUILD.md
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon="assets/icon.ico",   # uncomment once you have an .ico to use
)
