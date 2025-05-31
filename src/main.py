import copy
import os
import sys
import time
from copy import deepcopy
from pickletools import uint8
from typing import Optional

import win32gui, win32con, win32print
import numpy as np
import cv2
import pyautogui
from PySide6.QtCore import QRect
from PySide6.QtGui import QCloseEvent, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QDialog, QWidget
from PySide6 import QtGui, QtCore
import pyqtgraph
from loguru import logger as log

from ui.locate import Ui_Dialog_locate
from ui.mainwindow import Ui_MainWindow
from ui.preview import Ui_Widget_Preview
from data import DATA, Line, TYPE_IMAGE, ScoreDetections
from log import LogThread, init_log
from image_process import (detect_vertical_lines, detect_horizontal_lines,
                           save_image,read_image, image_pre_process, compare_image)

__version__ = "0.0.2"

class UI(QMainWindow, Ui_MainWindow):
    """
    处理UI响应和相关处理
    """

    def __init__(self, data, app: QApplication):
        self.data: DATA = data
        self.app = app
        super(UI, self).__init__()

        self.setupUi(self)
        self.setVisible(True)  # 设置可见后才可得到正确坐标值
        self.data.__init__(self.data.region.geometry_to_region(self.geometry()))  # 传递给数据类

        self.window_locate: Optional[WindowLocate] = None
        self.window_preview: Optional[WindowPreview] = None

        self.comboBox_log_level.currentTextChanged.connect(self.change_log_level)

        self.spinBox_region = [self.spinBox_region_x, self.spinBox_region_y,
                               self.spinBox_region_width, self.spinBox_region_height]
        self.console = self.textEdit_console

        # 初始化线程
        self.logThread = LogThread()
        self.capture_thread = CaptureThread(self.data)
        self.stitch_thread = StitchThread(self.data)
        self.reclip_thread = ReclipThread(self.data)

        # 限定输入框最大值
        self.spinBox_region_x.setMaximum(self.data.SCREEN_SIZE[0])
        self.spinBox_region_y.setMaximum(self.data.SCREEN_SIZE[1])
        self.spinBox_region_width.setMaximum(self.data.SCREEN_SIZE[0])
        self.spinBox_region_height.setMaximum(self.data.SCREEN_SIZE[1])

        # 绑定按钮响应函数
        self.pushButton_select_path.clicked.connect(self.select_path)
        self.pushButton_locate.clicked.connect(lambda: WindowLocate(self))
        self.pushButton_preview.clicked.connect(lambda: WindowPreview(self))
        self.pushButton_capture.clicked.connect(self.toggle_capture)
        self.pushButton_stitch.clicked.connect(self.start_stitch)
        self.pushButton_reclip.clicked.connect(self.start_reclip)

        self.init_data()


    def init_data(self) -> None:
        # 数据默认值初始化
        # file
        _file = sys.argv[0]  # 当编译后运行时，返回exe文件的路径
        for s in ["/", "\\", "\\\\"]:  # 初始化path，匹配三种目录表示方式
            if _file.rfind(f"{s}") >= 0:  # rfind()返回最后匹配值的索引
                self.data.exe_path = _file[:_file.rfind(f"{s}")]  # 执行文件所在目录
                self.data.ini_file = self.data.exe_path + s + "config.ini"
                self.data.score_save_path = self.data.exe_path + s + "output" + s
        # region
        self.data.region.set([self.frameGeometry().x(), self.frameGeometry().y(),
                              self.frameGeometry().width(), int(self.frameGeometry().height() / 3)])

        # 读取配置文件
        self.data.config.read_data_from_ini()

        # 切换程序工作目录
        try:
            os.chdir(self.data.score_save_path)
        except FileNotFoundError:
            os.mkdir(self.data.score_save_path)
            os.chdir(self.data.score_save_path)
        self.data.score_title = self.get_unused_filename(self.data.score_title)  # 必须置于目录创建后
        # log init
        self.logThread.signalForText.connect(self.output_log_to_ui)
        sys.stderr = self.logThread
        init_log(showlog_level=self.data.log_output_level)

        # 刷新范围显示
        self.flush_ui_display_data()

    def change_log_level(self) -> None:
        """更改log输出等级"""
        self.data.log_output_level = self.comboBox_log_level.currentText()
        init_log(showlog_level=self.data.log_output_level)
        log.info(f"Log level have changed to {self.data.log_output_level}")

    def toggle_capture(self) -> None:
        """切换截图开始状态，并调用相关函数"""

        def _start() -> bool:
            if not self.update_data_from_ui():  # 更新数据
                return False
            if self.data.score_title in os.listdir(self.data.score_save_path):  # 解决文件夹重名问题
                new_title = self.get_unused_filename(self.data.score_title)
                reply = QMessageBox.question(self, f"工作目录下已存在{self.data.score_title}文件夹",
                                             f"将修改曲谱标题，并新建文件夹{new_title}",
                                             QMessageBox.StandardButton.Yes,
                                             QMessageBox.StandardButton.Cancel)
                if reply == QMessageBox.StandardButton.Cancel:
                    return False
                self.data.score_title = new_title
                self.flush_ui_display_data()

            working_path = self.data.score_save_path + "\\" + self.data.score_title
            os.mkdir(working_path)
            working_path += "\\"  # 当前曲谱工作文件夹
            self.data.working_path = working_path
            init_log(sub_log_path=working_path, showlog_level=self.data.log_output_level)  # 添加子日志

            self.capture_thread.is_working = True
            self.capture_thread.start()  # 启动截图线程
            return True

        def _finished() -> None:
            self.pushButton_capture.setDisabled(False)  # 复位按钮状态
            self.capture_thread = CaptureThread(self.data)  # 创建新的线程，以供下次调用

        self.capture_thread.signal_finished.connect(_finished)
        if not self.capture_thread.is_working:
            if not _start():
                return
            self.pushButton_capture.setText("结束截图")
        else:
            self.pushButton_capture.setDisabled(True)  # 暂时禁用按钮
            self.pushButton_capture.setText("开始截图")
            self.capture_thread.signal_stop = True  # 发送停止信号

    def start_stitch(self) -> None:
        """启动图像拼接线程"""
        def _finished() -> None:
            self.stitch_thread = StitchThread(self.data) # 创建新的线程，以供下次调用

        if self.stitch_thread.is_working:
            QMessageBox.warning(self, f"警告",f"仍有拼接任务尚未完成，请稍后再试")
            return
        if not self.update_data_from_ui():
            return

        self.stitch_thread.is_working = True
        self.stitch_thread.signal_finished.connect(_finished)  # 绑定结束信号

        working_path = self.data.score_save_path + "\\" + self.data.score_title + "\\"
        self.data.working_path = working_path
        init_log(sub_log_path=working_path, showlog_level=self.data.log_output_level)  # 添加子日志

        self.stitch_thread.start()  # 启动截图线程

    def start_reclip(self) -> None:
        def _finished() -> None:
            self.reclip_thread = ReclipThread(self.data)

        if self.reclip_thread.is_working:
            QMessageBox.warning(self, f"警告",f"仍有重分割任务尚未完成，请稍后再试")
            return
        if not self.update_data_from_ui():
            return

        self.reclip_thread.is_working = True
        self.reclip_thread.signal_finished.connect(_finished)

        working_path = self.data.score_save_path + "\\" + self.data.score_title + "\\"
        self.data.working_path = working_path
        init_log(sub_log_path=working_path, showlog_level=self.data.log_output_level)  # 添加子日志

        self.reclip_thread.start()  # 启动截图线程

    def output_log_to_ui(self, text: str) -> None:
        """
        将text打印至ui中的plain text组件
        :param text:  输出的log字符
        """
        fmt = QtGui.QTextCharFormat()
        try:
            log_level = text.split("|")[1].strip()
        except IndexError:
            log_level = "ERROR"
        color = self.data.log_output_color.get(log_level)
        fmt.setForeground(QtGui.QBrush(QColor(color if color else "black")))  # 文字颜色,默认黑色
        self.console.mergeCurrentCharFormat(fmt)
        self.console.append(text[:-1])  # 去除结尾的换行符
        self.console.moveCursor(QtGui.QTextCursor.MoveOperation.End)  # 移动光标至末尾

    def select_path(self) -> None:
        """浏览并选择本地保存路径"""
        path = QFileDialog.getExistingDirectory(self)
        if path == "":
            return  # 当点击取消时，目录为空
        self.data.score_save_path = path
        os.chdir(self.data.score_save_path)  # 切换程序工作目录
        self.lineEdit_save_path.setText(path)

    def check_ui_input(self) -> bool:
        """检查ui输入数据的范围是否有效,并弹出相应的错误对话框"""
        # TODO 目录检查
        # 定位设置
        x, y, w, h = self.spinBox_region
        (max_width, max_height) = self.data.SCREEN_SIZE
        if int(x.value()) >= max_width or int(y.value()) >= max_height or \
                int(w.value()) == 0 or int(h.value()) == 0 or \
                int(w.value()) > max_width or int(h.value()) > max_height:
            QMessageBox.warning(self, "截图范围错误", "请重新输入主屏幕内有效坐标范围数据",
                                QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return False
        return True

    def update_data_from_ui(self, if_check: bool = True) -> bool:
        """检查并同步ui输入至DATA， 返回是否更新成功"""
        if if_check and (not self.check_ui_input()):  # 执行参数检查
            return False
        # 全局设置
        self.data.score_title = self.lineEdit_score_title.text()
        self.data.score_save_path = self.lineEdit_save_path.text()
        self.data.log_output_level = self.comboBox_log_level.currentText()
        try:
            os.chdir(self.data.score_save_path)  # 切换程序工作目录
        except FileNotFoundError:
            os.mkdir(self.data.score_save_path)
            os.chdir(self.data.score_save_path)
        self.data.score_save_format = self.comboBox_save_format.currentText()
        self.data.if_auto_manage_config = bool(self.checkBox_auto_manage_config.checkState().value)
        # 定位设置
        self.data.region.set([i.value() for i in self.spinBox_region])
        # 截图设置
        self.data.compare_method = self.comboBox_compare_method.currentText()
        self.data.compare_threshold = self.doubleSpinBox_compare_threshold.value()
        self.data.capture_delay = self.doubleSpinBox_capture_delay.value()
        self.data.if_keep_last = bool(self.checkBox_keep_last.checkState().value)
        self.data.if_reverse_image = bool(self.checkBox_reverse_image.checkState().value)
        # 图像识别设置
        self.data.horizontal_lines_num = self.spinBox_horizontal_lines_num.value()
        self.data.bar_lines_num = self.spinBox_bar_lines_num.value()

        return True

    def flush_ui_display_data(self) -> None:
        """刷新ui显示"""
        # 全局设置
        self.lineEdit_score_title.setText(self.data.score_title)
        self.lineEdit_save_path.setText(self.data.score_save_path)
        self.comboBox_save_format.setEditText(self.data.score_save_format)
        self.comboBox_log_level.setCurrentText(self.data.log_output_level)
        self.checkBox_auto_manage_config.setChecked(self.data.if_auto_manage_config)
        # 定位设置
        i = 0
        for w in self.spinBox_region:
            w.setValue(self.data.region[i])
            i += 1
        # 截图设置
        self.comboBox_compare_method.setCurrentText(self.data.compare_method)
        self.doubleSpinBox_compare_threshold.setValue(self.data.compare_threshold)
        self.doubleSpinBox_capture_delay.setValue(self.data.capture_delay)
        self.checkBox_keep_last.setChecked(self.data.if_keep_last)
        self.checkBox_reverse_image.setChecked(self.data.if_reverse_image)
        # 图像识别设置
        self.spinBox_horizontal_lines_num.setValue(self.data.horizontal_lines_num)
        self.spinBox_bar_lines_num.setValue(self.data.bar_lines_num)

    def get_unused_filename(self, filename: str, path: str = "") -> str:
        """
        在工作路径下查找文件名称是否占用，返回添加数字的版本以避免重名
        :param filename: 文件目录名称
        :param path:  查找路径
        :return: “filename+int(start form 0)”
        """

        if not path:
            path = self.data.score_save_path
        # 检测filename是否是以数字结尾
        if [i for i in [filename.rfind(i) for i in filename if i.isdigit()] if i == len(filename) - 1][:1]:
            # 获取最后一串数字中第一个数字的索引值
            index = [i for i in range(len(filename) - 1) if not filename[i].isdigit() and filename[i + 1].isdigit()][
                        -1] + 1
            filename, title_count = filename[:index], int(filename[index:])
        else:
            title_count = 0
        while True:  # title缺省值初始化
            folder_name = f"{filename}{title_count}"
            if folder_name in os.listdir(path):  # 避免重名
                title_count += 1
            else:
                break
        return folder_name

    def closeEvent(self, event: QCloseEvent, /) -> None:
        """重写窗口关闭事件，进行关闭前的后处理"""
        self.update_data_from_ui()
        self.data.config.save_config_to_ini()
        event.accept()


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
            self.ui.window_locate.activateWindow()  # 切换窗口焦点
            return
        self.ui.window_locate = self  # 赋值给主窗口，否则不显示

        super(WindowLocate, self).__init__()
        self.setupUi(self)

        self.setGeometry(self.data.region.region_to_geometry())

        self.pushButton_locate.clicked.connect(self.locate)
        self.pushButton_preview.clicked.connect(lambda: WindowPreview(self.ui))

        self.show()

    def locate(self) -> None:
        """
        定位范围，并更新显示
        """
        # TODO 多屏幕屏幕选择
        # 适配windows缩放
        hdc = win32gui.GetDC(0)  # 获取屏幕设备上下文
        dpi = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSX)  # 获取水平DPI
        win32gui.ReleaseDC(0, hdc)  # 释放资源
        scaling = dpi / 96.0  # 计算缩放比例（96 = 100% 缩放的标准 DPI）

        # 使用frameGeometry以包含标题栏尺寸
        region = [np.ceil(i*scaling) for i in self.data.region.geometry_to_region(self.frameGeometry())]

        # TODO 适配除win11下100%和125%缩放的准确性
        # 经测试，windows100%缩放下frameGeometry，标题栏上方会多出一个像素
        if scaling == 1:
            region[1] += 1  # y+1
            region[3] -= 1  # height-1

        self.data.region.set(region)
        self.ui.flush_ui_display_data()

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
        event.accept()  # 关闭窗口


class WindowPreview(QWidget, Ui_Widget_Preview):
    """
    预览窗口，继承自QDialog，创建实例时截取暂存并显示图片
    """

    def __init__(self, ui: UI):
        self.ui = ui
        self.data: DATA = self.ui.data
        if not self.ui.update_data_from_ui():  # 检查并更新region范围
            return
        if self.ui.window_preview is not None:
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
        self.pushButton_reverse_image.clicked.connect(lambda: self.show_image(255 - self.graphicsView.image))
        self.pushButton_update_image.clicked.connect(self.preview_region)
        self.pushButton_detect_lines.clicked.connect(self.show_lines_detected_image)

        self.graphicsView = self.graphWidget
        self.graphicsView.ui.histogram.hide()  # 隐藏直方图，菜单按钮，ROI
        self.graphicsView.ui.menuBtn.hide()
        self.graphicsView.ui.roiBtn.hide()

        self.preview_region()
        self.resize(int(self.data.image_preview.shape[1] * 1.5), int(self.data.image_preview.shape[0] * 2))

        self.show()
        self.graphicsView.autoRange()  # 自动缩放图片大小

    def preview_region(self) -> None:
        """显示region区域的预览"""
        if not self.ui.update_data_from_ui():  # 检查并更新region范围
            return
        print(self.data.region)
        log.info(self.data.region.tuple())
        img = image_pre_process(pyautogui.screenshot(region=self.data.region.tuple()), self.data)
        save_image("preview.png", img)
        self.data.image_preview = img
        self.show_image(self.data.image_preview)

    def show_image(self, img: TYPE_IMAGE) -> None:
        """在graph中显示传入的图片"""
        self.graphicsView.setImage(img)
        self.graphicsView.autoRange()  # 自动缩放图片大小

    def show_lines_detected_image(self):
        """显示预览图片的直线检测结果"""
        img = copy.deepcopy(self.data.image_preview)
        # img = copy.deepcopy(self.data.image_preview)
        grey_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        lines: list[Line] = []
        if self.comboBox.currentText() == "仅水平线":
            lines = detect_horizontal_lines(grey_img)
        elif self.comboBox.currentText() == "仅竖直线":
            lines = detect_vertical_lines(grey_img)
        elif self.comboBox.currentText() == "所有线段":
            lines = detect_horizontal_lines(grey_img)
            lines += detect_vertical_lines(grey_img, lines)
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
        event.accept()  # 关闭窗口



class CaptureThread(QtCore.QThread):
    """
    截图主进程
    """
    # 处理完毕信号
    signal_finished = QtCore.Signal()

    def __init__(self, data: DATA) -> None:
        super().__init__()
        self.data: DATA = data
        self.is_working: bool = False  # 主进程是否正在工作
        self.signal_stop: bool = False  # 中止线程信号

    def run(self) -> None:
        """线程入口启动函数，重写自run方法，使用.start()调用"""
        data: DATA = copy.deepcopy(self.data)  # 使用深拷贝，以保证data在执行中不变
        temp_list: list[np.ndarray] = []
        image_list: list[np.ndarray] = []
        image_count: int = -1  # 去重后输出的单张图像数量
        temp_count: int = -1  # 每轮阈值相同的循环
        total_count: int = -1  # 总截图张数
        time.sleep(0.5)  # 略微延时
        while True:  # 图片截取主循环
            temp_list.append(image_pre_process(pyautogui.screenshot(region=data.region.tuple()), data))
            temp_count += 1
            total_count += 1
            save_image(data.working_path + f"capture{total_count}{data.score_save_format}", temp_list[temp_count])
            if total_count == 0:
                log.info("===开始截图===")
            if temp_count == 0:  # 不过第一张图象不进行对比
                time.sleep(data.capture_delay)  # 延时
                continue

            # 将temp图像与上一张进行对比
            diff = compare_image(cv2.cvtColor(temp_list[temp_count], cv2.COLOR_RGB2GRAY),  # 转换为灰度图
                                 cv2.cvtColor(temp_list[temp_count - 1], cv2.COLOR_RGB2GRAY),
                                 data.compare_method)  # 指定算法
            # 与阈值相比较
            if data.compare_method == "SSIM":
                is_different = diff < data.compare_threshold
            elif data.compare_method == "MSE":
                is_different = diff > data.compare_threshold
            else:
                log.error("未知算法类型")
                return
            # 输出diff至log
            if is_different:
                log.info(f"{data.compare_method}-{str(total_count - 1)}-{str(total_count)}={str(round(diff, 5))}")
            else:
                log.debug(f"{data.compare_method}-{str(total_count - 1)}-{str(total_count)}={str(round(diff, 5))}")
            # 保存去重后的图像
            if is_different or (self.signal_stop and data.if_keep_last):  # 对最后一组进行保留
                if len(temp_list) > 2:  # 只保留缓存图像为三张以上的情况，以消除抖动
                    # 对temp图像取平均值，不计首尾两张，计算时转换格式为uint16，以避免求和数据溢出
                    image: np.ndarray = np.astype(np.average([np.array(i, dtype=np.uint16) for i in temp_list[1:-1]],
                                                             axis=0),  # 延0轴求和，保留图片数组形状
                                                  np.uint8)  # 转换回uint8格式
                    image_list.append(image)
                    image_count += 1
                    save_image(data.working_path + f"image{image_count}{data.score_save_format}", image)
                    log.success(f"output image{image_count} from "
                                f"capture{total_count - temp_count + 1}-{total_count - 1}")
                temp_list.clear()  # 清除缓存
                temp_count = -1  # 重置计数
            if self.signal_stop:  # 检测信号跳出循环
                self.signal_stop = False
                log.success("===本次截图完成===")
                self.signal_finished.emit()
                return
            time.sleep(data.capture_delay)  # 延时



class DetectThread(QtCore.QThread):
    """
    截图主进程
    """
    # 处理完毕信号

    signal_finished = QtCore.Signal()

    def __init__(self, data: DATA) -> None:
        super().__init__()
        self.data: DATA = data
        self.is_working: bool = False  # 主进程是否正在工作
        self.signal_stop: bool = False  # 中止线程信号

    def run(self) -> None:
        """线程入口启动函数，重写自run方法，使用.start()调用"""
        data: DATA = copy.deepcopy(self.data)  # 使用深拷贝，以保证data在执行中不变
        temp_list: list[np.ndarray] = []
        image_list: list[np.ndarray] = []


class StitchThread(QtCore.QThread):
    """
    图片拼接主进程
    """
    signal_finished = QtCore.Signal()  # 处理完毕信号

    def __init__(self, data: DATA):
        super().__init__()
        self.data: DATA = data
        self.is_working: bool = False  # 主进程是否正在工作

    def run(self):
        """线程入口启动函数，重写自run方法，使用.start()调用"""
        data = deepcopy(self.data)
        path = data.working_path
        score_detections = ScoreDetections(path, data.score_title)
        image_files:list[str] = []

        # 获取检测数据
        log.info("开始检测图像中的线段")
        for filename in os.listdir(path):
            if filename.rfind("image") >= 0:
                if filename.rfind("detected") >= 0:  # 移除检测过的图像
                    os.remove(os.path.join(path, filename))
                    continue
                image_files.append(filename)
                image_path = os.path.join(path, filename)
                image = read_image(image_path)
                image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                horizontal_lines = detect_horizontal_lines(image_gray)
                vertical_lines = detect_vertical_lines(image_gray, horizontal_lines)
                for l in horizontal_lines:
                    l.draw(image)
                for l in vertical_lines:
                    l.draw(image)
                save_image(path + "\\" + filename.split(".")[0] + "-detected" + data.score_save_format, image)
                score_detections.add_image(filename, horizontal_lines, vertical_lines)
                log.debug(f"{filename}-horizontal:{len(horizontal_lines)}-vertical:{len(vertical_lines)}")
        log.info("线段检测完毕，已生成对应预览图")

        # 排序图片
        image_format = "." + image_files[0].split(".")[-1]
        num = [int(f.split(".")[0].split("image")[-1]) for f in image_files]
        num.sort()
        image_names:list[str] = []
        for n in num:
            image_names.append("image"+str(n)+image_format)
        images = [read_image((os.path.join(path, i))) for i in image_names]  # 读取图片
        images_gray = [cv2.cvtColor(i, cv2.COLOR_RGB2GRAY) for i in images]

        # 获取mse最低时的拼接像素点
        log.info("比对图片中")
        stitch_points:list[int] = []
        for name_index in range(len(image_names) - 1):
            img1 = np.astype(images_gray[name_index], np.int8)  # ！！！避免差值数据溢出
            img2 = np.astype(images_gray[name_index + 1], np.int8)
            barline_index = score_detections[image_names[name_index]].get_lines_index(reverse=True)
            stitch_index = []
            for l in score_detections[image_names[name_index+1]].vertical_lines:
                stitch_index.append(barline_index + l.start_pixel)
            stitch_index = np.concatenate(stitch_index)
            stitch_index = np.unique(stitch_index)  # 对索引进行去重
            diff = [np.average(np.std(img1[:, -offset:] - img2[:, :offset])) for offset in stitch_index]  # 计算两张图像在offset区域中重叠差值的均值
            stitch_points.append(stitch_index[np.argmin(np.asarray(diff))] + 1)  # 右侧1像素为img2的部分
            log.debug(f"{image_names[name_index]}-{image_names[name_index + 1]}-stitch_point:{stitch_points[-1]}")
        log.info("图像比对完毕")

        # 进行拼接
        log.info("图像拼接中")
        images = [images[0]] + [images[i+1][:, stitch_points[i]:] for i in range(len(images)-1)]
        final_image = np.concatenate(images, axis=1)  # 延水平方向拼接
        result_file = data.working_path+data.score_title+"-stitched"+data.score_save_format
        save_image(result_file, final_image)
        log.info(f"图像拼接完毕，已生成预览图{result_file}")

        self.signal_finished.emit()






class ReclipThread(QtCore.QThread):
    """
    重分割主进程
    """

    signal_finished = QtCore.Signal()  # 处理完毕信号

    def __init__(self, data: DATA):
        super().__init__()
        self.data: DATA = data
        self.is_working: bool = False  # 主进程是否正在工作

    def run(self):
        """线程入口启动函数，重写自run方法，使用.start()调用"""
        log.debug("ReclicpThead:started")
        data = deepcopy(self.data)
        path = data.working_path
        stitched_image_file = data.score_title+"-stitched"+data.score_save_format
        stitched_detected_image_file = data.score_title+"-stitched"+"-detected"+data.score_save_format
        image_path = os.path.join(path, stitched_image_file)

        if stitched_image_file not in os.listdir(path):
            log.error(f"未在当前工作目录下发现{stitched_image_file}图片，请先进行拼接操作")
            self.signal_finished.emit()
            return
        if stitched_detected_image_file in os.listdir(path):  # 移除检测过的图像
            os.remove(os.path.join(path, stitched_detected_image_file))

        # 获取检测数据
        vertical_lines:list[Line] = []
        log.info("开始检测图像中的线段")
        image = read_image(os.path.join(path, stitched_image_file))
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        horizontal_lines = detect_horizontal_lines(image_gray)
        vertical_lines = detect_vertical_lines(image_gray, horizontal_lines)
        for l in horizontal_lines:
            l.draw(image)
        for l in vertical_lines:
            l.draw(image)
        save_image(os.path.join(path, stitched_detected_image_file), image)
        log.debug(f"horizontal:{len(horizontal_lines)}-vertical:{len(vertical_lines)}")
        log.info("线段检测完毕，已生成对应预览图")

        # 小节线分组
        index = np.asarray([l.start_pixel for l in vertical_lines])
        distance = index[1:] - index[:-1]
        for i in np.where(distance<np.average(distance)/5)[0]:
            vertical_lines[i].set_thickness(vertical_lines[i+1].end_pixel - vertical_lines[i].start_pixel)
            vertical_lines.pop(i+1)
        image = read_image(image_path)
        image_draw = deepcopy(image)
        for l in vertical_lines:
            l.draw(image_draw)
        save_image(path + "\\" + data.score_title + "-detected-barlines" + data.score_save_format, image_draw)
        log.info(f"{len(vertical_lines)}")

        # 进行切片
        clips = []
        extern_pixel = 4  # 左右额外包含的像素
        for i in range(4, len(vertical_lines)+1, 4):  # 从第四个小节开始，每四个小节
            if i == 4:  # 第一段
                clips.append(image[:, 0:vertical_lines[i].end_pixel + extern_pixel])
                continue
            # 中间段
            if i < len(vertical_lines):
                clips.append(image[:, vertical_lines[i-4].start_pixel - extern_pixel:
                                      vertical_lines[i].end_pixel + extern_pixel])
            if 1 < len(vertical_lines) - i < 4:  # 最后一段
                clips.append(image[:, vertical_lines[i].start_pixel - extern_pixel:
                                      vertical_lines[i].image_shape[1]])

        # 拼接
        canvas = np.ones_like(clips[np.argmax([c.size for c in clips])]).astype(np.uint8)*255
        canvas = np.concatenate([canvas for i in range(len(clips))], axis=0)  # 将画布的高度拓展len(clips)倍
        current_y = 0
        for c in clips:
            h = c.shape[0]
            w = c.shape[1]
            canvas[current_y:current_y+h, 0:w, :] = c
            current_y += h

        save_image(path + "\\" + data.score_title + "-reclip" + data.score_save_format, canvas)



        self.signal_finished.emit()




def show_main_window() -> None:
    """主窗口进程函数"""
    app = QApplication(sys.argv)
    window = UI(DATA(), app)
    window.show()
    window.activateWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    log.info("===main_start===")
    from test import detect_images, detect_image
    # detect_images(r"E:\dev_Code\Python\score_capture\output\untitled34")
    show_main_window()
    # detect_image("E:/dev_Code/Python/score_capture/src/output/untitled2/untitled2-stitched.jpg")
    log.info("===main_finish===")
