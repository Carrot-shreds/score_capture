import sys
from loguru import logger as log
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore

from __init__ import __version__
from Model.data import DATA
from ViewModel.MainWindow import UI

@log.catch()
def show_main_window() -> None:
    """主窗口进程函数"""
    # dps缩放设定，详见https://doc.qt.io/qtforpython-6/PySide6/QtCore/Qt.html#PySide6.QtCore.Qt.HighDpiScaleFactorRoundingPolicy
    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)  # default

    app = QApplication(sys.argv)
    window = UI(DATA(), app)
    window.show()
    window.activateWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    log.info("===main_start===")
    log.info(f"Current version: {__version__}")
    show_main_window()
    log.info("===main_finish===")
