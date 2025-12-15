import os
import sys
import time
import copy
import shutil
import subprocess
from copy import deepcopy
from typing import Optional

import cv2
import mss
import numpy as np
import pyqtgraph
import PySide6.QtCore
from PySide6.QtCore import QRect
from PySide6.QtGui import QCloseEvent, QColor, QTextCursor, QTextCharFormat, QBrush, QGuiApplication
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QDialog, QWidget, QInputDialog
from PySide6 import QtCore
from loguru import logger as log

from ui.locate_ui import Ui_Dialog_locate
from ui.mainwindow_ui import Ui_MainWindow
from ui.preview_ui import Ui_Widget_Preview
from ui.stitch_ui import Ui_Widget_Stitch
from data import DATA, LITERAL_DIRECTIONS, CaptureData, Line, TYPE_IMAGE, ScoreDetections, StitchData
from log import LogThread, init_log
from image_process import (detect_vertical_lines, detect_horizontal_lines,
                           image_pre_process, compare_image,
                           get_barline_num_region, detect_all_lines_with_clip, clip_image, stitch_images)
from utilities import (is_valid_filename, order_filenames, read_numbered_image_names, open_folder_in_explorer,
                        read_numbered_images, rename_files, read_image, save_image, screenshot)

__version__ = "0.1.2"

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
    show_main_window()
    log.info("===main_finish===")
