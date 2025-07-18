import re
import os
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
    def extract_number(filename: str) -> int:
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

