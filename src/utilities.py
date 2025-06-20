import re

def is_valid_filename(filename: str) -> bool:
    """
    检查给定的文件名是否有效。
    有效的文件名不应包含以下任何字符：
    \ /： *？ “ <> |不应以空间或点结尾。
    """
    invalid_chars = r'[\\/:*?"<>|]'
    if re.search(invalid_chars, filename) or filename.endswith((' ', '.')):
        return False
    return True

