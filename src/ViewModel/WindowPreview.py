from copy import deepcopy
from typing import Optional

import cv2
import numpy as np
import pyqtgraph
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QWidget
from loguru import logger as log

from . import MainWindow
from view.preview_ui import Ui_Widget_Preview

from Model.data import DATA, Line, TYPE_IMAGE
from Model.image_process import detect_vertical_lines, detect_horizontal_lines, image_pre_process
from Model.utils import save_image, screenshot

class WindowPreview(QWidget, Ui_Widget_Preview):
    """
    预览窗口，继承自QDialog，创建实例时截取暂存并显示图片
    """

    def __init__(self, ui: MainWindow.UI):
        self.ui = ui
        self.data: DATA = self.ui.data
        if not self.ui.update_data_from_ui():  # 检查并更新region范围
            return
        if self.ui.window_preview is not None:
            self.ui.window_preview.showNormal()  # 从最小化恢复窗口显示
            self.ui.window_preview.activateWindow()  # 切换窗口焦点
            self.ui.window_preview.preview_region()
            return
        self.ui.window_preview = self  # 赋值给主窗口，否则不显示

        # 在setupUi()前完成对pyqt_graph的配置
        if np.average(self.data.image_preview) < 128:  # 当图片亮度均值偏小时，设置背景为白色
            pyqtgraph.setConfigOption("background", "w")  # 默认背景为黑色
            pyqtgraph.setConfigOption("foreground", "w")  # 统一前景色
        pyqtgraph.setConfigOption("imageAxisOrder", "row-major")  # 设置图像显示以行为主（横置）

        super().__init__()
        self.setupUi(self)

        self.pushButton_clear_lines.clicked.connect(lambda: self.show_image(self.data.image_preview))
        self.pushButton_reverse_image.clicked.connect(lambda: self.show_image(255 - self.graphicsView.image 
                                                                              if self.graphicsView.image is not None
                                                                                else self.data.image_preview))
        self.pushButton_update_image.clicked.connect(self.preview_region)
        self.pushButton_detect_lines.clicked.connect(self.show_lines_detected_image)

        self.graphicsView = self.graphWidget
        self.graphicsView.ui.histogram.hide()  # 隐藏直方图，菜单按钮，ROI
        self.graphicsView.ui.menuBtn.hide()
        self.graphicsView.ui.roiBtn.hide()

        self.preview_region()
        self.resize(min(int(self.data.image_preview.shape[1] * 1.5), self.data.SCREEN_SIZE[0]),
            min(int(self.data.image_preview.shape[0] * 2), self.data.SCREEN_SIZE[1]))

        self.show()
        self.graphicsView.autoRange()  # 自动缩放图片大小

    def preview_region(self) -> None:
        """显示region区域的预览"""
        if not self.ui.update_data_from_ui():  # 检查并更新region范围
            return
        print(self.data.region)
        log.debug(f"preview region: {self.data.region.get_tuple()}")
        img = image_pre_process(
            screenshot(region=self.data.region.get_tuple(), capture_tool=self.data.capture_tool
            ), self.data)
        save_image("preview.png", img)
        self.data.image_preview = img
        self.show_image(self.data.image_preview)

    def show_image(self, img: TYPE_IMAGE) -> None:
        """在graph中显示传入的图片"""
        self.graphicsView.setImage(img)
        self.graphicsView.autoRange()  # 自动缩放图片大小

    def show_lines_detected_image(self):
        """显示预览图片的直线检测结果"""
        if not self.ui.update_data_from_ui():
            return
        img = deepcopy(self.data.image_preview)
        # img = copy.deepcopy(self.data.image_preview)
        grey_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        lines: list[Line] = []
        if self.comboBox.currentText() == "仅水平线":
            lines = detect_horizontal_lines(grey_img, self.data.detect_coefficient_horizontal)
        elif self.comboBox.currentText() == "仅竖直线":
            lines = detect_vertical_lines(grey_img, coefficient=self.data.detect_coefficient_vertical)
        elif self.comboBox.currentText() == "所有线段":
            lines = detect_horizontal_lines(grey_img, self.data.detect_coefficient_horizontal)
            lines += detect_vertical_lines(grey_img, lines, self.data.detect_coefficient_vertical)
        for line in lines:
            line.draw(img)  # 记得转换回RGB
        self.show_image(img)
        save_image("preview_linesDetected.png", img)

    def closeEvent(self, event: Optional[QCloseEvent]) -> None:
        """
        重写窗口关闭事件
        :param event: 窗口关闭事件
        """
        self.ui.window_preview = None
        if event is not None:
            event.accept()  # 关闭窗口

