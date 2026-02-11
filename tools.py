import argparse
import subprocess
import sys
from pathlib import Path

from loguru import logger as log

SCRIPTS_PATH = {
    # update source tr tag to translations files
    "lupdate": Path("./src/resource/translations/update_ts.py").as_posix(),
    # compile .ts file to .qm file
    "lrelease": Path("./src/resource/translations/compile_qm.py").as_posix(),
    # compile designer .ui file to .py file
    "uic": Path("./src/View/ui/ui_compile.py").as_posix(),
    # compile .qrc source file to .py
    "rcc": Path("./src/resource/compile_qrc.py").as_posix(),
    # QtDesigner for editing ui file
    "designer": list(Path("./.venv/Scripts").glob("pyside6-designer.*"))[0].as_posix(),
    # QtLinguist for translsting ts` file
    "linguist": list(Path("./.venv/Scripts").glob("pyside6-linguist.*"))[0].as_posix(),
    "build": "",
}


def build():
    run_script("lrelease")
    run_script("rcc")
    run_script("uic")


def run_script(name: str):
    if (path := SCRIPTS_PATH[name]) != "":
        if path.split(".")[-1] == "py":
            subprocess.run([sys.executable, path])
        else:
            subprocess.run(path)
        return
    match name:
        case "build":
            build()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", help="Update translation source to ts files.")
    args = parser.parse_args()
    if (cmd := args.cmd) in SCRIPTS_PATH.keys():
        run_script(cmd)
    else:
        log.error(f"Unknown command, should in {list(SCRIPTS_PATH.keys())}")


if __name__ == "__main__":
    main()
