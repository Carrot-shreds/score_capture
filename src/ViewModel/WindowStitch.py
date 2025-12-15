import os
import time
from typing import Optional

import numpy as np
import pyqtgraph
from loguru import logger as log
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QFileDialog, QWidget

from . import MainWindow
from view.stitch_ui import Ui_Widget_Stitch

from Model.data import DATA, LITERAL_DIRECTIONS, StitchData
from Model.log import init_log
from Model.image_process import stitch_images
from Model.utils import read_numbered_image_names, read_numbered_images, save_image

class WindowStitch(QWidget, Ui_Widget_Stitch):
    """
    拼接窗口，继承自QDialog，手动调整拼接点并实时显示stitched图像
    """

    def __init__(self, ui: MainWindow.UI):
        self.ui: MainWindow.UI = ui
        if not self.ui.update_data_from_ui():  # 检查并更新数据
            return
        self.data: DATA = self.ui.data
        if self.ui.window_stitch is not None:
            self.ui.window_stitch.showNormal()  # 从最小化恢复窗口显示
            self.ui.window_stitch.activateWindow()  # 切换窗口焦点
            return
        self.ui.window_stitch = self  # 赋值给主窗口，否则不显示

        self.path: str = os.path.join(self.data.score_save_path, self.data.score_title)
        self.image_names: list[str] 
        self.images: list[np.ndarray] 
        self.stitched_image: np.ndarray
        self.stitched_image_length = lambda: self.stitched_image.shape[1] if self.stitch_direction == "horizontal" else self.stitched_image.shape[0]
        self.stitchData_filename:str
        self.stitchData: StitchData
        self.stitch_points: list[int] 
        self.stitch_direction: LITERAL_DIRECTIONS
        self.show_region: tuple[int, int]

        # 在setupUi()前完成对pyqt_graph的配置
        if np.average(self.data.image_preview) < 128:  # 当图片亮度均值偏小时，设置背景为白色
            pyqtgraph.setConfigOption("background", "w")  # 默认背景为黑色
            pyqtgraph.setConfigOption("foreground", "w")  # 统一前景色
        pyqtgraph.setConfigOption(
            "imageAxisOrder", "row-major")  # 设置图像显示以行为主（横置）

        super().__init__()
        self.setupUi(self)

        self.spinBox_stitch_points_index.valueChanged.connect(self.change_point_index)
        self.spinBox_stitch_points_value.valueChanged.connect(self.change_point_value)

        self.pushButton_open_file.clicked.connect(self.open_file)
        self.pushButton_save_file.clicked.connect(self.save_file)
        self.pushButton_save_image.clicked.connect(self.save_image)

        self.imageView = self.graphWidget
        self.viewbox = self.imageView.getView()
        # self.graphicsView.ui.histogram.hide()  # 显示直方图，隐藏菜单按钮，ROI
        self.imageView.ui.menuBtn.hide()
        self.imageView.ui.roiBtn.hide()

        self.resize(int(self.data.SCREEN_SIZE[0] * 0.5),
                     int(self.data.SCREEN_SIZE[1] * 0.3))
        self.move(int(self.data.SCREEN_SIZE[0] * 0.1),
                     int(self.data.SCREEN_SIZE[1] * 0.1))
        self.show()

        if os.path.exists(self.path) and "StitchData.json" in os.listdir(self.path):
            self.load_stitch_points(os.path.join(self.path, "StitchData.json"))
            self.flush_stitch_preview()
        else:
            log.warning(f"未在{self.path}下发现StitchData.json文件，请先进行一次拼接操作")

    def image_length(self, index: int = 0) -> int:
        """返回指定index的image的宽度或高度"""
        if self.stitch_direction == "horizontal":
            return self.images[index].shape[1]
        elif self.stitch_direction == "vertical":
            return self.images[index].shape[0]
        return 0

    def open_file(self) -> None:
        if not self.ui.update_data_from_ui():  # 更新数据:
            return
        self.data = self.ui.data
        filename = QFileDialog.getOpenFileName(
            self, 
            dir=os.path.join(self.ui.data.score_save_path, self.ui.data.score_title) 
            if os.path.exists(os.path.join(self.ui.data.score_save_path, self.ui.data.score_title))
            else self.ui.data.score_save_path, 
            filter="JSON files (*.json *.JSON)")[0]
        if filename == "":
            return  # 当点击取消时，目录为空
        
        self.load_stitch_points(filename)
        log.info("成功打开文件:"+filename)
        self.flush_stitch_preview()

    def load_stitch_points(self, file: str) -> None:
        if file == "" or not os.path.exists(file):
            log.error("不存在文件:"+file)
            return
        if os.path.dirname(file) != self.path:
            init_log(sub_log_path=os.path.dirname(file),
                     showlog_level=self.ui.data.log_output_level)  # 添加子日志
        self.path = os.path.dirname(file)
        self.image_names = read_numbered_image_names(self.path, "image")
        if self.image_names == []:
            log.error("打开文件失败:"+file)
            return

        self.images = read_numbered_images(self.path, "image", self.image_names)
        self.stitchData = StitchData.load_from_file(file)
        self.stitchData_filename = file
        self.stitch_points = self.stitchData.points
        self.stitch_direction = self.stitchData.stitch_direction
        # 先resize再调整显示范围
        self.resize(min(int(self.images[0].shape[1]), self.data.SCREEN_SIZE[0]),  
                    min(int(self.images[0].shape[0]+100), self.data.SCREEN_SIZE[1]))
        if self.stitch_direction == "horizontal":  # 初始图片显示范围
            self.show_region = (0, int(self.viewbox.width()))  
        elif self.stitch_direction == "vertical":
            self.show_region = (0, int(self.viewbox.height()))
        log.info(f"成功加载拼接点数据，共{len(self.images)}张图片，{len(self.stitch_points)}个拼接点")
        log.debug(f"Stitch Points: {[(n, self.stitch_points[n]) for n in range(len(self.stitch_points))]}")

        # 限制输入框范围
        self.spinBox_stitch_points_index.setMaximum(len(self.stitch_points)-1)
        self.spinBox_stitch_points_index.setValue(0)
        self.change_point_index()

    def save_file(self) -> None:
        name = f"StitchData_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json"
        self.stitchData.save_to_file(os.path.join(self.path, name))
        log.success(f"已保存拼接点数据至{os.path.join(self.path, name)}")
    
    def save_image(self) -> None:
        if not os.path.exists(self.path):
            log.error(f"指定路径不存在: {self.path}")
            return
        name = f"{self.data.score_title}-stitched{self.data.score_save_format}"
        save_image(os.path.join(self.path, name), self.stitched_image)
        log.success(f"已保存拼接预览图像至{os.path.join(self.path,name)}")

    def show_image(self, img: np.ndarray) -> None:
        """在graph中显示传入的图片"""
        self.imageView.setImage(img)
        # 设置显示样式
        if self.stitch_direction == "horizontal":
            # 关闭缩放锁定
            self.viewbox.setAspectLocked(False)
            # 仅允许x轴缩放
            self.viewbox.setMouseEnabled(x=True, y=False)
            self.viewbox.setLimits(xMin=0, xMax=img.shape[1])
            # y轴自动适应缩放
            self.viewbox.enableAutoRange(axis='y', enable=True)
            self.viewbox.setAutoVisible(y=True)
            self.viewbox.setAutoPan(y=True)  # 不写这个会导致移动缩放闪烁bug
            self.viewbox.setXRange(self.show_region[0], self.show_region[1] ,padding=0)
        elif self.stitch_direction == "vertical":
            # 关闭缩放锁定
            self.viewbox.setAspectLocked(False)
            # 仅允许y轴缩放
            self.viewbox.setMouseEnabled(x=False, y=True)
            self.viewbox.setLimits(yMin=0, yMax=img.shape[0])
            # x轴自动适应缩放
            self.viewbox.enableAutoRange(axis="x", enable=True)
            self.viewbox.setAutoVisible(x=True)
            self.viewbox.setAutoPan(x=True)  # 不写这个会导致移动缩放闪烁bug
            self.viewbox.setYRange(self.show_region[0], self.show_region[1], padding=0)

    def flush_stitch_preview(self) -> None:
        self.stitched_image = stitch_images(self.images, self.stitch_points, self.stitch_direction)
        point_position: int = self.image_length(0)
        point_position += sum([self.image_length(i) - self.stitch_points[i] for i in range(self.spinBox_stitch_points_index.value())])
        if point_position not in range(self.show_region[0], self.show_region[1]):
            blank = int(self.viewbox.width()/2) if self.stitch_direction == "horizontal" else int(self.viewbox.height()/2)
            self.show_region = (max(0, point_position-blank), min(point_position+blank, self.stitched_image_length()))
        self.show_image(self.stitched_image)

    def change_point_index(self) -> None:
        # 以下三行代码不能调换先后顺序
        self.spinBox_stitch_points_value.setMaximum(self.image_length(self.spinBox_stitch_points_index.value()+1))
        self.spinBox_stitch_points_value.setValue(self.stitch_points[self.spinBox_stitch_points_index.value()])
        self.spinBox_stitch_points_value.setMinimum(1)
        self.flush_stitch_preview()

    def change_point_value(self) -> None:
        self.stitch_points[self.spinBox_stitch_points_index.value()] = self.spinBox_stitch_points_value.value()
        self.stitchData.points[self.spinBox_stitch_points_index.value()] = self.spinBox_stitch_points_value.value()
        self.flush_stitch_preview()

    def closeEvent(self, event: Optional[QCloseEvent]) -> None:
        """
        重写窗口关闭事件
        :param event: 窗口关闭事件
        """
        self.ui.window_stitch = None
        if event is not None:
            event.accept()  # 关闭窗口
