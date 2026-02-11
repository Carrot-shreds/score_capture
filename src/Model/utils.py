import hashlib
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Literal, overload

import cv2
import mss
import numpy as np
from fontTools.ttLib import TTFont
from loguru import logger as log
from pydantic import validate_call
from pydantic_extra_types.color import Color
from PySide6 import QtCore
from PySide6.QtCore import QRect
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication, QDialog, QMainWindow

from src.Model.Data.const import CaptureTool
from src.Model.Data.type import (
    DirectoryExisting,
    FileName,
    ImageArray,
    ImageFileName,
    ImagePath,
    RegionData,
)


def is_valid_filename(filename: str) -> bool:
    """
    检查给定的文件名是否有效。
    是否包含非法字符，或以空格或点结尾。
    """
    invalid_chars = r'[\\/:*?"<>|]'
    if re.search(invalid_chars, filename) or filename.endswith((" ", ".")):
        return False
    return True


def extract_filename_number(filename: str) -> int | float:
    match = re.search(r"(\d+)", filename)
    return int(match.group(0)) if match else float("inf")


@validate_call
def order_filenames(filenames: list[FileName]) -> list[FileName]:
    """
    对文件名进行排序，确保数字部分正确排序。
    例如：['file1.txt', 'file10.txt', 'file2.txt'] -> ['file1.txt', 'file2.txt', 'file10.txt']
    """
    return sorted(filenames, key=extract_filename_number)


@validate_call
def order_path(path: list[Path]) -> list[Path]:
    return sorted(path, key=lambda v: extract_filename_number(v.name))


@validate_call
def rename_files(
    path: DirectoryExisting,
    old_filenames: list[FileName],
    new_filenames: list[FileName],
) -> None:
    """
    重命名文件，将old_filenames中的文件重命名为new_filenames中的对应名称。
    """
    if len(old_filenames) != len(new_filenames):
        raise ValueError(
            QApplication.translate(
                "rename_files", "Old and New filenames list have different length."
            )
        )

    # 检查新文件名是否与旧文件名相同
    for old, new in list(zip(old_filenames, new_filenames)):
        if old == new:
            old_filenames.remove(old)
            new_filenames.remove(new)
    if new_filenames == []:
        log.info(
            QApplication.translate(
                "rename_files", "There are no file needed to rename."
            )
        )
        return

    temp_filenames = [filename + ".tmp" for filename in new_filenames]
    # 先将所有文件重命名为.tmp文件，避免重命名冲突
    for old_name, temp_name in zip(old_filenames, temp_filenames):
        (path / old_name).rename(path / temp_name)

    for old_name, temp_name, new_name in zip(
        old_filenames, temp_filenames, new_filenames
    ):
        (path / temp_name).rename(path / new_name)
        log.info(
            QApplication.translate("rename_files", "Renamed file {} -> {}").format(
                old_name, new_name
            )
        )


@validate_call
def reorder_image_files(path: DirectoryExisting, filename: ImageFileName) -> None:
    """
    对指定路径下的图像文件进行重新排序和重命名。
    """
    file_names = os.listdir(path)
    file_names = [
        f
        for f in file_names
        if f.rfind(filename) > -1 and f.split(".")[0].split(filename)[-1].isdigit()
    ]
    if file_names == []:
        log.warning(
            QApplication.translate(
                "reorder_image_files", "No {} related file found."
            ).format(filename)
        )
        return
    ordered_filenames = order_filenames(file_names)

    image_format = ordered_filenames[0].split(".")[-1]
    for n in range(len(ordered_filenames)):
        ordered_filenames[n] = f"{filename}{n}.{image_format}"

    rename_files(path, file_names, ordered_filenames)


@validate_call
def save_image(imagepath: ImagePath, img: ImageArray) -> None:
    """支持中文路径的cv图片存储"""
    image_format = "." + imagepath.name.split(".")[-1]  # 获取文件格式
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imencode(image_format, np.asarray(img))[1].tofile(imagepath)


@validate_call
def read_image(
    imagepath: ImagePath, color: Literal["RGB", "GRAY"] = "RGB"
) -> ImageArray:
    """支持中文路径的cv图片读取"""
    img = cv2.imdecode(np.fromfile(imagepath, dtype=np.uint8), -1)
    if img is None:
        raise ValueError("Empty image data")
    if color == "RGB":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if color == "GRAY":
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return img


@validate_call
def get_numbered_image_names(
    path: DirectoryExisting, name_without_num: str, order_names: bool = True
) -> list[str]:
    """读取指定路径下按数字排序的图像文件名列表"""
    file_names = os.listdir(path)
    pattern = re.compile(rf"^{name_without_num}[0-9]+\.(?i:jpg|jpeg|png|bmp|tiff)$")
    file_names = [f for f in file_names if pattern.match(f)]
    if file_names == []:
        # log.warning(f"没有在当前工作路径下找到{name_without_num}相关的图像文件")
        return []
    if order_names:
        file_names = order_filenames(file_names)
    return file_names


@overload
def read_images(
    path: DirectoryExisting, filenames: list[ImageFileName]
) -> list[ImageArray]: ...


@overload
def read_images(path: list[ImagePath]) -> list[ImageArray]: ...


@validate_call
def read_images(
    path: DirectoryExisting | list[ImagePath],
    filenames: list[ImageFileName] | None = None,
) -> list[ImageArray]:
    if isinstance(path, Path) and filenames:
        return [read_image(path / f) for f in filenames]
    elif isinstance(path, list):
        return [read_image(p) for p in path]
    else:
        raise ValueError("Invalid Input Arguments")


@validate_call
def read_numbered_images(
    path: DirectoryExisting,
    name_without_num: str,
    image_file_names: list[ImageFileName] | None = None,
) -> list[ImageArray]:
    """读取指定路径下按数字排序的图像列表"""
    if image_file_names is None:
        filenames = get_numbered_image_names(path, name_without_num)
    else:
        filenames = image_file_names
    if filenames == []:
        return []
    return read_images(path, filenames)


@validate_call
def hash_image(image: ImageArray) -> str:
    """计算图像的MD5 hash值"""
    image_bytes = image.tobytes()
    return hashlib.md5(image_bytes).hexdigest()


@validate_call
def open_folder_in_explorer(folder_path: DirectoryExisting) -> None:
    """在文件资源管理器中打开指定文件夹"""
    match sys.platform:
        case "win32":  # Windows
            os.startfile(folder_path)
        case "darwin":  # macOS
            if err := subprocess.run(["open", folder_path], capture_output=True).stderr:
                log.error(f"Reveal folder failed: {err.decode()}")
        case "linux":  # Linux
            if err := subprocess.run(
                ["xdg-open", folder_path], capture_output=True
            ).stderr:
                log.error(f"Reveal folder failed: {err.decode()}")
        case _:
            log.error(f"Unsupport system: {sys.platform}")


def qrect2tuple(rect: QRect) -> tuple[int, int, int, int]:
    return rect.x(), rect.y(), rect.width(), rect.height()


def qrect2array(rect: QRect) -> np.ndarray:
    return np.asarray(qrect2tuple(rect))


@validate_call
def screenshot(
    region_data: RegionData, capture_tool: CaptureTool = CaptureTool.MSS
) -> ImageArray:
    """截取屏幕指定区域的截图"""
    # mss暂时不支持Wayland桌面环境
    region, monitor_num = region_data.region, region_data.monitor_num
    if capture_tool != CaptureTool.MSS:
        temp_filename: str = f"captureTEMP{time.time()}.png"
        match capture_tool:
            case CaptureTool.GRIM:
                result = subprocess.run(
                    ["grim", "-o", temp_filename], capture_output=True
                )
            case CaptureTool.SPECTACLE:
                result = subprocess.run(
                    [
                        "spectacle",
                        "--current",
                        "--background",
                        "--nonotify",
                        "--fullscreen",
                        "--output",
                        temp_filename,
                    ],
                    capture_output=True,
                )
        if result.stderr:
            log.error(
                QApplication.translate(
                    "screenshot", "Capture Failed using {}: {}"
                ).format(capture_tool, result.stderr.decode())
            )
            return np.array([])
        # TODO Linux 兼容性测试
        img = read_image(Path(temp_filename))
        os.remove(temp_filename)
        img = img[region[1] : region[1] + region[3], region[0] : region[0] + region[2]]
        return img

    with mss.mss() as sct:
        monitors = sct.monitors
        if monitor_num < 1 or monitor_num >= len(monitors):
            log.error(
                QApplication.translate("screenshot", "Invalid Monitor Number").format(
                    monitor_num
                )
            )
            return np.array([])
        monitor = monitors[monitor_num]
        left, top, width, height = region
        capture_region = {
            "left": monitor["left"] + left,
            "top": monitor["top"] + top,
            "width": width,
            "height": height,
        }
        sct_img = sct.grab(capture_region)
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        return img


@validate_call
def get_unused_filename(filename: str, dir: DirectoryExisting) -> str:
    """
    在工作路径下查找文件名称是否占用，返回添加数字的版本以避免重名
    :param filename: 文件目录名称
    :param path:  查找路径
    :return: “filename+int(start form 0)”
    """
    # 检测filename是否是以数字结尾
    if [
        i
        for i in [filename.rfind(i) for i in filename if i.isdigit()]
        if i == len(filename) - 1
    ][:1]:
        # 获取最后一串数字中第一个数字的索引值
        index = [
            i
            for i in range(len(filename) - 1)
            if not filename[i].isdigit() and filename[i + 1].isdigit()
        ][-1] + 1
        filename, title_count = filename[:index], int(filename[index:])
    else:
        title_count = 0
    while True:  # title缺省值初始化
        folder_name = f"{filename}{title_count}"
        if folder_name in os.listdir(dir):  # 避免重名
            title_count += 1
        else:
            break
    return folder_name


def set_window_always_on_top(window: QMainWindow | QDialog, state: bool) -> None:
    """设置窗口置顶状态"""
    if window.windowHandle():
        window.windowHandle().setFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, state)
        window.update()
    else:
        # When creating window
        window.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, state)
        # window.show() in outside


def color2bgr(color: Color) -> tuple[int, int, int]:
    rgb_color = color.__getattribute__("_rgba")
    return (int(rgb_color.b * 255), int(rgb_color.g * 255), int(rgb_color.r * 255))


def color2rgb(color: Color) -> tuple[int, int, int]:
    rgb_color = color.__getattribute__("_rgba")
    return (int(rgb_color.r * 255), int(rgb_color.g * 255), int(rgb_color.b * 255))


def fill_image_border(
    src: ImageArray, shape: tuple[int, ...], color: Color
) -> ImageArray:
    left = int((shape[1] - src.shape[1]) / 2)
    right = int(shape[1] - src.shape[1] - left)
    top = int((shape[0] - src.shape[0]) / 2)
    bottom = int(shape[0] - src.shape[0] - top)
    return cv2.copyMakeBorder(
        src, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color2rgb(color)
    )


def unify_image_shape(images: list[ImageArray], color: Color) -> list[ImageArray]:
    shape = np.max([i.shape[0] for i in images]), np.max([i.shape[1] for i in images])
    return [fill_image_border(i, shape, color) for i in images]


def get_sysfonts() -> dict[str, Path]:
    # From Pillow ImageFont.truetype()
    dirs: list[str] = []
    if sys.platform == "win32":
        # check the windows font repository
        # NOTE: must use uppercase WINDIR, to work around bugs in
        # 1.5.2's os.environ.get()
        windir = os.environ.get("WINDIR")
        if windir:
            dirs.append(os.path.join(windir, "fonts"))
        if local := os.environ.get("LOCALAPPDATA"):
            local_font_dir = Path(local) / "microsoft" / "windows" / "fonts"
            if local_font_dir.exists():
                dirs.append(local_font_dir.as_posix())
    elif sys.platform in ("linux", "linux2"):
        data_home = os.environ.get("XDG_DATA_HOME")
        if not data_home:
            # The freedesktop spec defines the following default directory for
            # when XDG_DATA_HOME is unset or empty. This user-level directory
            # takes precedence over system-level directories.
            data_home = os.path.expanduser("~/.local/share")
        xdg_dirs = [data_home]

        data_dirs = os.environ.get("XDG_DATA_DIRS")
        if not data_dirs:
            # Similarly, defaults are defined for the system-level directories
            data_dirs = "/usr/local/share:/usr/share"
        xdg_dirs += data_dirs.split(":")

        dirs += [os.path.join(xdg_dir, "fonts") for xdg_dir in xdg_dirs]
    elif sys.platform == "darwin":
        dirs += [
            "/Library/Fonts",
            "/System/Library/Fonts",
            os.path.expanduser("~/Library/Fonts"),
        ]

    font_info: dict[str, Path] = {}
    for d in dirs:
        for file in Path(d).iterdir():
            if file.suffix.lower() != ".ttf":
                continue
            font = TTFont(file)
            name_table = font["name"]
            for i in name_table.names:
                if i.nameID == 1:
                    font_name = i.toStr()
            font_info[font_name] = file
    return font_info


def ndarray2qimage(img: ImageArray) -> QImage:
    return QImage(
        img.data,
        img.shape[1],
        img.shape[0],
        img.shape[1] * 3,
        QImage.Format.Format_RGB888,
    )
