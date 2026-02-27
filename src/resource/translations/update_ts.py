import subprocess
from pathlib import Path

src: Path = Path(__file__).parent.parent.parent
files = [src.parent / "main.py"]
ts_files = ["zh_CN.ts"]
ts_files = [(src / "resource" / "translations" / f).as_posix() for f in ts_files]


def get_files(path: Path):
    for p in path.iterdir():
        if p.is_dir():
            if p.name in ["output", "resource", "__pycache__"]:
                continue
            get_files(p)
        if p.name == "__init__.py" or p.name.find("ui_.py") >= 0:
            continue
        if p.suffix in [".py", ".ui", ".qml"]:
            files.append(p.as_posix())


get_files(src)
cmd = ["pyside6-lupdate"] + files + ["-no-obsolete"] + ["-ts"] + ts_files
print(f"files: {files}")
subprocess.run(cmd)
