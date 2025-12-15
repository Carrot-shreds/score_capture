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

class WindowLocate(QDialog, Ui_Dialog_locate):
    """
    定位窗口，继承自QDialog
    """

    def __init__(self, ui: UI):
        self.ui = ui
        self.data: DATA = self.ui.data
        if not self.ui.update_data_from_ui():  # 检查并更新region范围
            return
        if self.ui.window_locate is not None:
            self.ui.window_locate.setGeometry(
                self.data.region.region_to_geometry(  # 重设窗口位置
                without_title_frame=True))
            self.ui.window_locate.showNormal()  # 从最小化恢复窗口显示
            self.ui.window_locate.activateWindow()  # 切换窗口焦点
            return
        self.ui.window_locate = self  # 赋值给主窗口属性，否则无法显示

        super(WindowLocate, self).__init__()
        self.setupUi(self)

        self.setGeometry(self.data.region.region_to_geometry())

        self.pushButton_locate.clicked.connect(self.locate)
        self.pushButton_preview.clicked.connect(lambda: WindowPreview(self.ui))

        self.setWindowFlag(QtCore.Qt.WindowType.WindowMinimizeButtonHint, True)  # 为窗口添加最小化按钮

        self.show()

    def locate(self) -> None:
        """
        定位范围，并更新显示
        """
        # TODO 多屏幕屏幕选择
        scaling = 1

        if sys.platform == "win32":
            scaling = self.ui.screen().devicePixelRatio()  # 获取缩放比例
            self.data.region_offset = np.asarray([0,np.round(1*scaling),0,np.round(-1*scaling)])  # Win11测试结果
        if sys.platform == "linux":
            self.data.region_offset = np.asarray([0,0,-1,-1])  # Arch/KDE测试结果

        # 使用frameGeometry以包含标题栏尺寸
        region = np.asarray([np.ceil(i*scaling)
            for i in self.data.region.geometry_to_region(self.frameGeometry())])

        region += self.data.region_offset  # 加上偏移值,默认为0,0,0,0
        self.data.region.set(region)
        self.ui.flush_ui_display_data()

        log.debug(f"screen scaling: {scaling}")
        log.debug(f"region offset: {self.data.region_offset}")
        log.success(f"update region: {self.data.region.get_tuple()}")

    def setGeometry(self, a0: QRect) -> None:
        """
        经测试原始方法设置的坐标值会有偏差，分别使用move和resize重写
        """
        self.move(a0.x(), a0.y())
        self.resize(a0.width(), a0.height())

    def closeEvent(self, event: Optional[QCloseEvent]) -> None:
        """
        重写窗口关闭事件
        :param event: 窗口关闭事件
        """
        self.ui.window_locate = None
        if event is not None:
            event.accept()  # 关闭窗口

