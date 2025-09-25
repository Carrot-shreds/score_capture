import re
import os
import sys
import cv2
import time
import mss
import subprocess
from typing import Literal
import numpy as np
import hashlib
from loguru import logger as log

def is_valid_filename(filename: str) -> bool:
    """
    检查给定的文件名是否有效。
    是否包含非法字符，或以空格或点结尾。
    """
    invalid_chars = r'[\\/:*?"<>|]'
    if re.search(invalid_chars, filename) or filename.endswith((' ', '.')):
        return False
    return True

def order_filenames(filenames: list[str]) -> list[str]:
    """
    对文件名进行排序，确保数字部分正确排序。
    例如：['file1.txt', 'file10.txt', 'file2.txt'] -> ['file1.txt', 'file2.txt', 'file10.txt']
    """
    def extract_number(filename: str) -> int | float:
        match = re.search(r'(\d+)', filename)
        return int(match.group(0)) if match else float('inf')

    return sorted(filenames, key=extract_number)

def rename_files(path: str, old_filenames: list[str], new_filenames: list[str]) -> None:
    """
    重命名文件，将old_filenames中的文件重命名为new_filenames中的对应名称。
    """
    if len(old_filenames) != len(new_filenames):
        raise ValueError("旧文件名和新文件名列表长度不匹配")
    
    # 检查新文件名是否与旧文件名相同
    filename_couple = list(zip(old_filenames, new_filenames))
    for old, new in filename_couple:
        if old == new:
            old_filenames.remove(old)
            new_filenames.remove(new)
    if new_filenames == []:
        log.info("没有需要重命名的文件")
        return

    temp_filenames = [filename+".tmp" for filename in new_filenames]
    # 先将所有文件重命名为.tmp文件，避免重命名冲突
    for old_name, temp_name, new_name in zip(old_filenames, temp_filenames, new_filenames):
        if not is_valid_filename(new_name):
            raise ValueError(f"无效的新文件名: {new_name}")
        os.rename(os.path.join(path, old_name), os.path.join(path, temp_name))

    for old_name, temp_name, new_name in zip(old_filenames, temp_filenames, new_filenames):
        os.rename(os.path.join(path, temp_name), os.path.join(path, new_name))
        log.info(f"成功将'{old_name}'重命名为'{new_name}'")

def reorder_image_files(path: str, filename: str) -> None:
    """
    对指定路径下的图像文件进行重新排序和重命名。
    """
    if not os.path.exists(path):
        log.error(f"指定路径不存在: {path}")
        return

    file_names = os.listdir(path)
    file_names = [f for f in file_names
                   if f.rfind(filename) > -1 and 
                      f.split(".")[0].split(filename)[-1].isdigit()]
    if file_names == []:
        log.warning(f"没有在当前工作路径下找到{filename}相关的图像文件")
        return
    ordered_filenames = order_filenames(file_names)

    image_format = ordered_filenames[0].split(".")[-1]
    for n in range(len(ordered_filenames)):
        ordered_filenames[n] = f"{filename}{n}.{image_format}"

    rename_files(path, file_names, ordered_filenames)

def save_image(filepath: str, img: np.ndarray) -> None:
    """支持中文路径的cv图片存储"""
    image_format = "." + filepath.split(".")[-1]  # 获取文件格式
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imencode(f"{image_format}", np.asarray(img))[1].tofile(filepath)


def read_image(filepath: str, color: Literal["RGB", "BGR", "GRAY"] = "RGB") -> np.ndarray:
    """支持中文路径的cv图片读取"""
    img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), -1)
    if color == "RGB":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if color == "GRAY":
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return np.asarray(img)

def read_numbered_image_names(path: str, name_without_num: str, order_names:bool = True) -> list[str]:
    """读取指定路径下按数字排序的图像文件名列表"""
    if not os.path.exists(path):
        log.error(f"指定路径不存在: {path}")
        return []

    file_names = os.listdir(path)
    pattern = re.compile(
        rf'^{name_without_num}[0-9]+\.(?i:jpg|jpeg|png|bmp|tiff)$')
    file_names = [f for f in file_names if pattern.match(f)]
    if file_names == []:
        log.warning(f"没有在当前工作路径下找到{name_without_num}相关的图像文件")
        return []
    if order_names:
        file_names = order_filenames(file_names)
    return file_names

def read_numbered_images(path: str, name_without_num: str, 
                         image_file_names: list[str] | None = None) -> list[np.ndarray]:
    """读取指定路径下按数字排序的图像列表"""
    if image_file_names is None:
        filenames = read_numbered_image_names(path, name_without_num)
    else:
        filenames = image_file_names
    if filenames == []:
        return []
    return [read_image(os.path.join(path, f)) for f in filenames]

def hash_image(image: np.ndarray) -> str:
    """计算图像的MD5 hash值"""
    image_bytes = image.tobytes()
    return hashlib.md5(image_bytes).hexdigest()

def open_folder_in_explorer(folder_path: str) -> None:
    """在文件资源管理器中打开指定文件夹"""
    match sys.platform:
        case "win32":  # Windows
            os.startfile(folder_path)
        case "darwin":  # macOS
            if err:=subprocess.run(['open', folder_path], capture_output=True).stderr:
                log.error(f"无法打开文件夹: {err.decode()}")
        case "linux":  # Linux
            if err:=subprocess.run(['xdg-open', folder_path], capture_output=True).stderr:
                log.error(f"无法打开文件夹: {err.decode()}")    
        case _:
            log.error(f"不支持的操作系统: {sys.platform}")
        

def screenshot(region:tuple[int,int,int,int], capture_tool:str="mss", monitor_num:int=1) -> np.ndarray:
    """截取屏幕指定区域的截图"""
    # mss在Wayland下无法使用
    if capture_tool != "mss":
        temp_filename: str = f"captureTEMP{time.time()}.png"
        match capture_tool:
            case "grim":
                result=subprocess.run(["grim", "-o", temp_filename], capture_output=True)
            case "spectacle":   
                result=subprocess.run(
                    ["spectacle","--current","--background", "--nonotify", "--fullscreen", "--output", temp_filename], 
                    capture_output=True)
            case _:
                log.error(f"不支持的截图工具: {capture_tool}")
        if result.stderr:
            log.error(f"{capture_tool}截图失败: {result.stderr.decode()}")
            return np.array([])
        img = read_image(temp_filename)
        os.remove(temp_filename)
        img = img[region[1]:region[1]+region[3],
                                        region[0]:region[0]+region[2]]
        return img
    
    with mss.mss() as sct:
        monitors = sct.monitors
        if monitor_num < 1 or monitor_num >= len(monitors):
            log.error(f"无效的显示器编号: {monitor_num}")
            return np.array([])
        monitor = monitors[monitor_num]
        left, top, width, height = region
        capture_region = {
            "left": monitor["left"] + left,
            "top": monitor["top"] + top,
            "width": width,
            "height": height
        }
        sct_img = sct.grab(capture_region)
        img = np.array(sct_img)
        # img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        return img
