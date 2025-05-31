from typing import Optional
import sys

from PySide6 import QtCore
from loguru import logger as log

class LogThread(QtCore.QThread):
    """log输出线程"""
    signalForText = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def write(self, text):
        """将文本输出传输至信号"""
        self.signalForText.emit(str(text))

    def flush(self) -> None:
        """什么都不用做，但是没有这个函数的声明的话pycharm调试器会报错"""
        pass

def init_log(showlog_level: str = "INFO", sub_log_path: Optional[str] = None) -> None:
    """

    :param sub_log_path: 保存的子日志的路径
    :param showlog_level: UI显示的日志等级
    """
    _format_save = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> ' \
                   '| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<yellow>{line}</yellow> - <level>{message}</level>'
    _format_show = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> ' \
                   '| <level>{message}</level>'
    try:
        if log.ids:
            for i in log.ids:
                log.remove(i)  # 清除所有配置
            log.ids = []
    except AttributeError:
        log.ids = []  # 首次调用时声明变量
    log.ids.append(log.add(sys.stdout, level=showlog_level, format=_format_show))  # 控制台输出日志
    log.ids.append(log.add("logs.txt", level="DEBUG", format=_format_save, encoding="UTF-8",
                           enqueue=True))  # 主日志，保存所有DEBUG日志到程序根目录下
    log.ids.append(log.add(sys.stderr, level=showlog_level, format=_format_show))  # 显示在UI中的日志进程
    if sub_log_path is not None:
        log.ids.append(log.add(sub_log_path + "\\log.txt", level="DEBUG", format=_format_save, encoding="UTF-8",
                               enqueue=True))  # 每次工作目录中单开的子日志

