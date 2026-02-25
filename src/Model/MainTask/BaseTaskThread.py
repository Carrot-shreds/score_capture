from abc import abstractmethod
from threading import get_native_id

from loguru import logger as log
from PySide6.QtCore import QThread

from src.Model.Data.type import Directory
from src.Model.log import logManager


def log_fliter_thread_id(record, id) -> bool:
    return record["extra"].get("thread_id") == id


class BaseTaskThread(QThread):
    working_dir: Directory

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def main(self, logger) -> None: ...

    def run(self) -> None:
        """线程入口启动函数，重写自run方法，使用.start()调用"""
        self.finished.connect(self.deleteLater)
        logger = log
        log_file = self.working_dir / "log.txt"
        try:
            id = get_native_id()
            logManager.add_log_config(
                sink=log_file,
                filter=lambda v: log_fliter_thread_id(v, id),
            )
            logger = log.bind(thread_id=id)
            self.main(logger)  # Call Main Function
        except Exception as e:
            import traceback

            title = self.tr("{} Error: {}").format(type(self).__name__, e.__repr__())
            logger.error(title)
            logger.error(traceback.format_exc())
        finally:
            logManager.remove_log_config(log_file)
