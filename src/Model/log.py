import logging
import sys
from typing import Any, Callable, TextIO

from loguru import logger as log
from PySide6.QtCore import QObject, Signal

from src.Model.Data.const import LogLevel
from src.Model.Data.settings import LogSettings
from src.Model.Data.type import LogPath, Singleton


class LoggingInterceptHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record: logging.LogRecord):
        try:  # Get the log level
            level = log.level(record.levelname).name
        except ValueError:
            level = record.levelno
        if "pyffmpeg" in record.name:
            level = LogLevel.DEBUG  # show all ffmpeg logs as debug

        # detour logging message to loguru
        log.log(level, record.getMessage())


class LogToGui(QObject):
    """Log text output to gui tab"""

    signalForText = Signal(str)

    def __init__(self):
        super().__init__()
        self.buffer_text: list[str] = []
        self.buffer_mode: bool = True

    def write(self, text):
        """emit text through qt signal"""
        self.signalForText.emit(str(text))
        if self.buffer_mode:
            self.buffer_text.append(text)

    def flush(self) -> None:
        """solve pycharm debuger warning"""
        pass

    def clear_buffer(self):
        if self.buffer_text:
            [self.signalForText.emit(str(t)) for t in self.buffer_text]
            self.buffer_mode = False


class MyStdout(TextIO):
    def __init__(self, original: TextIO, output_level=LogLevel.DEBUG):
        super().__init__()
        self.original: TextIO = original
        self.output_level = output_level
        self._buffer: str = ""

    def write(self, text):
        self._buffer += text
        if "\n" in self._buffer:
            lines = self._buffer.split("\n")
            for line in lines[:-1]:  # The final line may be not finished
                if line:  # Ignore empty lines
                    log.log(self.output_level, line)
            self._buffer = lines[-1]  # Keep last part

    def flush(self) -> None:
        if self._buffer:
            log.log(self.output_level, self._buffer)
            self._buffer = ""


@Singleton
class LogManager:
    def __init__(self) -> None:
        sys.stdout = MyStdout(sys.stdout)
        self.detour_logging()
        self.logToGui = LogToGui()
        self.log_settings = None
        self.myStderr = MyStdout(sys.stderr, LogLevel.ERROR)

    def detour_logging(self) -> None:
        from pyffmpeg import logger

        for handler in logger.handlers[:]:  # use slice copy for loop
            logger.removeHandler(handler)  # remove pyffmpeg's stderr handler
        logging.basicConfig(  # detour logging output, no debug log
            handlers=[LoggingInterceptHandler()],
            level=logging.INFO,
            force=True,  # Remove the default stderr output
        )

    @property
    def log_config(self) -> dict[str, list[dict[str, Any]]]:
        return self._log_config

    @log_config.setter
    def log_config(self, value):
        self._log_config = value
        self.apply_log_config()

    def init_log_settings(self, log_settings: LogSettings):
        self.log_settings = log_settings
        self._log_config = self.generate_config()
        self.apply_log_config()
        # Hook stderr after loguru add the original stderr sink.
        sys.stderr = self.myStderr

    def generate_config(self):
        if not self.log_settings:
            return
        return {
            "handlers": [
                {
                    "sink": self.myStderr.original,
                    "level": LogLevel.DEBUG,
                    "format": self.log_settings.show_format,
                },
                {
                    "sink": self.logToGui,
                    "level": LogLevel.DEBUG,
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
        sink: LogPath | TextIO | LogToGui,
        filter: Callable | None = None,
        level: LogLevel | None = None,
        format: str | None = None,
        config: dict | None = None,
    ) -> None:
        if not self.log_settings:
            return
        if not config:
            config = self.log_config
        handler = {
            "sink": sink,
            "level": level if level is not None else self.log_settings.save_level,
            "format": format if level is not None else self.log_settings.save_format,
            "filter": filter,
        }
        if sink is LogPath:
            handler["encoding"] = "UTF-8"
            handler["enqueue"] = True
        config["handlers"].append(handler)
        self.log_config = config

    def remove_log_config(
        self, sink: LogPath | TextIO | LogToGui, config: dict | None = None
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


logManager = LogManager()
