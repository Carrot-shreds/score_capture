import sys
from typing import Any, Callable, TextIO

from loguru import logger as log
from PySide6.QtCore import QThread, Signal

from src.Model.Data.const import LogLevel
from src.Model.Data.settings import LogSettings, logSettings
from src.Model.Data.type import Singleton, TxtPath


class LogThread(QThread):
    """log输出线程"""

    signalForText = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def write(self, text):
        """将文本输出传输至信号"""
        self.signalForText.emit(str(text))

    def flush(self) -> None:
        """什么都不用做，但是没有这个函数的声明的话pycharm调试器会报错"""
        pass


class stderr2loguru:
    def write(self, text):
        if text != "":
            log.error(text.strip())

    def flush(self) -> None:
        pass


@Singleton
class LogManager:
    def __init__(self, log_settings: LogSettings) -> None:
        sys.stderr = stderr2loguru()
        self.log_settings = log_settings
        self._log_config = self.generate_config()
        self.apply_log_config()

    @property
    def log_config(self) -> dict[str, list[dict[str, Any]]]:
        return self._log_config

    @log_config.setter
    def log_config(self, value):
        self._log_config = value
        self.apply_log_config()

    def generate_config(self):
        return {
            "handlers": [
                {
                    "sink": sys.stdout,
                    "level": self.log_settings.show_level,
                    "format": self.log_settings.show_format,
                },
                {
                    "sink": self.log_settings.log_path,
                    "rotation": self.log_settings.log_main_rotation,
                    "retention": self.log_settings.log_main_retention,
                    "level": self.log_settings.save_level,
                    "format": self.log_settings.save_format,
                    "encoding": "UTF-8",
                    "enqueue": True,
                },
            ],
        }

    def add_log_config(
        self,
        sink: TxtPath | TextIO | LogThread,
        filter: Callable | None = None,
        level: LogLevel | None = None,
        format: str | None = None,
        config: dict | None = None,
    ) -> None:
        if not config:
            config = self.log_config
        handler = {
            "sink": sink,
            "level": level if level is not None else self.log_settings.save_level,
            "format": format if level is not None else self.log_settings.save_format,
            "filter": filter,
        }
        if sink is TxtPath:
            handler["encoding"] = "UTF-8"
            handler["enqueue"] = True
        config["handlers"].append(handler)
        self.log_config = config

    def remove_log_config(
        self, sink: TxtPath | TextIO | LogThread, config: dict | None = None
    ) -> None:
        if not config:
            config = self.log_config
        config["handlers"] = [h for h in config["handlers"] if h.get("sink") != sink]
        self.log_config = config

    def apply_log_config(self, config: dict | None = None) -> None:
        if not config:
            config = self.log_config
        log.remove()  # Remove all log handlers added so far, including the default
        log.configure(**config)  # type:ignore


logManager = LogManager(logSettings)
