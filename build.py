import datetime
import os
import subprocess
from pathlib import Path
from shutil import rmtree

from loguru import logger as log

from src import __version__ as version


def build():
    path = os.getcwd()
    if "src" in os.listdir(path):
        path += "\\src"
    else:
        log.error("未在当前目录下发现src文件夹，请将build脚本置于src的上级目录")
        return
    log.info(f"将编译{path}下的所有.py文件")

    files = []
    for fspath, dirs, fs in os.walk(path):
        for f in fs:
            files.append(os.path.join(fspath, f))
    files = [f for f in files if os.path.isfile(f) and f.split(".")[-1] == "py"]
    log.info(files)

    command = [
        "cmd",
        "/c",
        "nuitka",
        "--standalone",
        # "--disable-console",
        "--clang",
        "--msvc=latest",
        "--enable-plugin=pyside6",
        "--remove-output",
        "--output-dir=build",
        "--report=build/build_report.xml",
        "--output-filename=score_capture.exe",
        "--include-qt-plugins=platforminputcontexts",
        "--include-module="
        + ",".join(
            ["src"]
            # [
            #     os.path.split(i)[-1].split(".")[0]
            #     for i in files
            #     if not i.count("main.py")
            # ]
        ),
        "main.py",
    ]
    log.info(command)

    subprocess.run(command)
    if not (Path(".") / "build" / "main.dist" / "score_capture.exe").exists():
        rmtree(Path(".") / "build" / "main.dist")
        return

    folder_name = f"score_capture-{version}-build-" + datetime.datetime.now().strftime(
        "%y%m%d_%H%M"
    )
    if "main.dist" in os.listdir(os.getcwd() + "\\build\\"):
        os.rename(
            os.getcwd() + "\\build\\main.dist", os.getcwd() + f"\\build\\{folder_name}"
        )
    log.info("output: " + os.getcwd() + f"\\build\\{folder_name}")
    log.info("build finished")


if __name__ == "__main__":
    build()
