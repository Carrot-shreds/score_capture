import datetime
import os
import subprocess
from pathlib import Path
from shutil import rmtree

from loguru import logger as log

from src import __version__ as version

delete_files = [
    "qt6network.dll",
    "qt6qml.dll",
    "qt6qmlmodels.dll",
    "qt6quick.dll",
    "cv2/opencv_videoio_ffmpeg4130_64.dll",
]


def build():
    command = [
        "cmd",
        "/c",
        "nuitka",
        "--standalone",
        "--windows-console-mode=disable",
        "--clang",
        "--msvc=latest",
        "--enable-plugin=pyside6",
        # "--remove-output",
        "--output-dir=build",
        "--report=build/build_report.xml",
        "--output-filename=score_capture.exe",
        "--windows-icon-from-ico=./src/resource/media/score_capture.jpg",
        "--macos-app-icon=./src/resource/media/score_capture.jpg",
        "--include-qt-plugins=platforminputcontexts",
        "--include-module=src",
        "main.py",
    ]
    log.info(command)

    subprocess.run(command)

    # if compile failed
    if (
        Path("./build/main.dist").exists()
        and not Path("./build/main.dist/score_capture.exe").exists()
    ):
        rmtree(Path("./build/main.dist"))
        return

    folder_name = f"score_capture-{version}-build-" + datetime.datetime.now().strftime(
        "%y%m%d_%H%M"
    )
    if Path("./build/main.dist").exists():
        out_path = Path(f"./build/{folder_name}")
        Path("./build/main.dist").rename(out_path)
        log.info("output: " + out_path.as_posix())
        for d in delete_files:
            if (file := (out_path / d)).exists():
                os.remove(file)
                log.debug(f"File Removed: {d}")

    log.info("build finished")


if __name__ == "__main__":
    build()
