import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["pygame"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("Fire_Escape.py", base=base)]

setup(
    name = "Fire Escape",
    version = "0.1",
    description = "Fire Escape Game",
    options = {"build_exe": build_exe_options},
    executables = executables
)