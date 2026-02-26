import argparse
import datetime
import os
import platform
import shutil
import subprocess
import sys
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

platform_name = {"win32": "windows", "darwin": "macos", "linux": "linux"}
arch_name = {"AMD64": "x86_64"}


def get_platform() -> str:
    return platform_name[sys.platform]


def get_arch() -> str:
    return arch_name[platform.machine()]


def make_folder_name(debug: bool) -> str:
    # like "score_capture-0.2.0-windows-x86_64"
    # or "score_capture-0.2.0-windows-x86_64-debug-260226_0221"
    name = f"score_capture-{version}-{get_platform()}-{get_arch()}"
    if debug:
        name += "-debug-" + datetime.datetime.now().strftime("%y%m%d_%H%M")
    return name


def build(debug: bool = True, clean_output: bool = False, pack_archive: bool = True):
    log.info(f"Building mode: {'debug' if debug else 'release'}")

    # get upx path
    result = subprocess.run(["where", "upx"], capture_output=True, text=True)
    if result.returncode != 0:
        log.warning("Upx unavailable. Check your system path.")

    command = [
        "cmd",
        "/c",
        "nuitka",
        "--standalone",
        "--clang",
        "--msvc=latest",
        "--enable-plugin=pyside6,upx",
        "--onefile-no-compression",
        "--include-qt-plugins=platforminputcontexts",
        "--windows-console-mode=disable" if not debug else "",
        "--lto=yes" if not debug else "",  # Link time optimization
        "--unstripped" if debug else "--strip",  # keep traceback data for debug
        "--remove-output" if clean_output else "",
        "--output-dir=build",
        "--report=build/build_report.xml",
        "--include-data-files=LICENSE=LICENSE",
        "--include-data-files=README.md=README.md",
        "--include-data-dir=docs=docs",
        "--output-filename=score_capture.exe",
        "--windows-icon-from-ico=./src/resource/media/score_capture.jpg",
        "--macos-app-icon=./src/resource/media/score_capture.jpg",
        f"--file-version={version}",
        f"--product-version={version}",
        "--file-description=Score Capture",
        "--copyright=Copyright © 2025 Carrot-shreds",
        "--include-module=src",
        "main.py",
    ]
    command = [cmd for cmd in command if cmd != ""]
    log.info(command)

    subprocess.run(command)

    # if compile failed
    if (
        Path("./build/main.dist").exists()
        and not Path("./build/main.dist/score_capture.exe").exists()
    ):
        rmtree(Path("./build/main.dist"))
        return

    if not Path("./build/main.dist").exists():
        return

    # Rename Folder
    folder_name = make_folder_name(debug)
    out_path = Path(f"./build/{folder_name}")
    if out_path.exists():
        shutil.rmtree(out_path)
    Path("./build/main.dist").rename(out_path)
    log.info("output: " + out_path.as_posix())

    # Delete unused files.
    for d in delete_files:
        if (file := (out_path / d)).exists():
            os.remove(file)
            log.debug(f"File Removed: {d}")

    # Pack zip
    if pack_archive:
        log.info("Packing Zip file.")
        shutil.make_archive(
            base_name=(Path("./build") / folder_name).resolve().as_posix(),
            format="zip",
            root_dir=out_path.resolve(),  # the root dir of the packed archive and base_dir.
            base_dir=Path("."),  # the folder will be packed, based on root_dir.
        )

    log.info("build finished")


def bool_arg(arg) -> bool:
    if isinstance(arg, bool):
        return arg
    if isinstance(arg, str):
        if arg.lower() in ["true", "1"]:
            return True
        elif arg.lower() in ["false", "0"]:
            return False
        else:
            raise ValueError(f"Can not cast {arg} to a bool value.")
    elif isinstance(arg, int):
        return bool(arg)
    else:
        raise TypeError(f"Unsupport arg type {type(arg)}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", help="debug or release", type=str, required=False, default="debug"
    )
    parser.add_argument(
        "--clean_output",
        help="Clean the output cache after building.",
        type=bool_arg,
        default=False,
        required=False,
    )
    parser.add_argument(
        "--pack_archive",
        help="Pack a zip file after building.",
        type=bool_arg,
        default=True,
        required=False,
    )

    args = parser.parse_args()
    log.debug(args.__repr__().split("(")[1:][0].split(")")[:-1][0])
    if args.mode.lower() == "debug":
        build(
            debug=True, clean_output=args.clean_output, pack_archive=args.pack_archive
        )
    elif args.mode.lower() == "release":
        build(
            debug=False, clean_output=args.clean_output, pack_archive=args.pack_archive
        )
    else:
        log.error("Invaild build mode, shuold be 'debug' or 'release'.")
