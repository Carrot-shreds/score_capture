import subprocess
from pathlib import Path

source = []
target = []
for f in Path(__file__).parent.glob("*.ts"):
    source.append(f.as_posix())
    target.append(f.with_suffix(".qm").as_posix())

print(f"{source=}")
print(f"{target=}")
for s, t in zip(source, target):
    cmd = ["pyside6-lrelease", s, "-qm", t]
    subprocess.run(cmd)
