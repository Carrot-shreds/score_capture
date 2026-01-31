import sys

from loguru import logger as log
from PySide6 import QtCore
from PySide6.QtWidgets import QApplication

from src import __version__
from src.ViewModel.MainWindow import MainWindow_VM


@log.catch()
def show_main_window() -> None:
    """主窗口进程函数"""
    # dps缩放设定，详见https://doc.qt.io/qtforpython-6/PySide6/QtCore/Qt.html#PySide6.QtCore.Qt.HighDpiScaleFactorRoundingPolicy
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )  # default

    # Ignore Error - "qt.qpa.window: SetProcessDpiAwarenessContext() failed"
    QtCore.QLoggingCategory.setFilterRules("qt.qpa.window.warning=false")
    app = QApplication(sys.argv)
    window = MainWindow_VM()
    window.show()
    window.activateWindow()
    app.exec()


if __name__ == "__main__":
    log.info("===main_start===")
    log.info(f"Current version: {__version__}")
    show_main_window()
    log.info("===main_finish===")
