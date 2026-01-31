from pydantic_extra_types.color import Color
from PySide6.QtGui import (
    QBrush,
    QColor,
    QTextCharFormat,
    QTextCursor,
)

from src.Model.Data.const import LogLevel
from src.Model.Data.settings import logSettings
from src.Model.log import LogThread, logManager
from src.View import TabConsole_View
from src.ViewModel.binding.bind_data import bind_data


class TabConsole_VM(TabConsole_View):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainWindow = parent
        self.logSettings = logSettings
        self.logManager = logManager

        self.logThread = LogThread()
        self.logThread.signalForText.connect(self.output_log_text)
        self.logManager.add_log_config(
            self.logThread,
            level=LogLevel.DEBUG,
            format=self.logSettings.show_format,
        )

        self.pushButton_clear_console.clicked.connect(self.clear_console)
        bind_data(self.checkBox_auto_scroll, self.logSettings, "auto_scroll")
        bind_data(self.comboBox_log_level, self.logSettings, "show_level")

    def fliter_log_level(self, log_level: str, fliter_level: str) -> bool:
        order = ["debug", "info", "success", "warning", "error"]
        return order.index(log_level.lower()) >= order.index(fliter_level.lower())

    def output_log_text(self, text: str) -> None:
        """
        将text打印至ui中的plain text组件
        :param text:  输出的log字符
        """
        fmt = QTextCharFormat()
        try:
            log_level = text.split("|")[1].strip().lower()
        except IndexError:
            log_level = "error"
        if not self.fliter_log_level(log_level, self.logSettings.show_level):
            return
        color = self.logSettings.color_config.__dict__.get(log_level, "black")
        if isinstance(color, Color):
            color = QColor(*color.as_rgb_tuple())
        else:
            color = QColor(color)
        fmt.setForeground(QBrush(color))  # 文字颜色,默认黑色
        self.textEdit_console.mergeCurrentCharFormat(fmt)
        self.textEdit_console.append(text[:-1])  # 去除结尾的换行符
        if self.logSettings.auto_scroll:
            self.textEdit_console.moveCursor(
                QTextCursor.MoveOperation.End
            )  # 移动光标至末尾

    def clear_console(self) -> None:
        self.textEdit_console.clear()
