import subprocess
import sys
from pathlib import Path

cwd: Path = Path(__file__).parent
for p in cwd.glob("*.ui"):
    ui_file = p.resolve()
    py_file = (cwd / (p.name.split(".ui")[0] + "_ui.py")).resolve()
    cmd = ["pyside6-uic", ui_file, "-o", py_file]
    subprocess.run(cmd)
    print(ui_file)
    print(py_file)
