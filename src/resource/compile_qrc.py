import subprocess
from pathlib import Path

cwd: Path = Path(__file__).parent
if (qrc := cwd / "resource.qrc").exists():
    py_file = cwd / "compiled_resource.py"
    cmd = ["pyside6-rcc", qrc.as_posix(), "-o", py_file.as_posix()]
    subprocess.run(cmd)
    print(f"compiled {qrc} to {py_file}")
