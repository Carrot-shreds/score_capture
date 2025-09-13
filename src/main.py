import copy
import os
import shutil
import sys
import time
from copy import deepcopy
from typing import Optional

import win32gui
import win32con
import win32print
import numpy as np
import cv2
import pyautogui
import PySide6.QtCore
from PySide6.QtCore import QRect
from PySide6.QtGui import QCloseEvent, QColor, QTextCursor, QTextCharFormat, QBrush
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QDialog, QWidget, QInputDialog
from PySide6 import QtCore
import pyqtgraph
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
from utilities import is_valid_filename, order_filenames, read_numbered_image_names, read_numbered_images, rename_files, read_image, save_image

__version__ = "0.1.1"


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

        # 子窗口声明
        self.window_locate: Optional[WindowLocate] = None
        self.window_preview: Optional[WindowPreview] = None
        self.window_stitch: Optional[WindowStitch] = None
        self.spinBox_region = [self.spinBox_region_x, self.spinBox_region_y,
                               self.spinBox_region_width, self.spinBox_region_height]
        self.console = self.textEdit_console

        # 初始化线程
        self.logThread = LogThread()
        self.capture_thread = CaptureThread(self.data)
        self.buildimage_thread = BuildImageThread(self.data)
        self.stitch_thread = StitchThread(self.data)
        self.reclip_thread = ReclipThread(self.data)

        # 限定输入框最大值
        self.spinBox_region_x.setMaximum(self.data.SCREEN_SIZE[0])
        self.spinBox_region_y.setMaximum(self.data.SCREEN_SIZE[1])
        self.spinBox_region_width.setMaximum(self.data.SCREEN_SIZE[0])
        self.spinBox_region_height.setMaximum(self.data.SCREEN_SIZE[1])

        # 绑定响应函数
        # 全局设置
        self.pushButton_select_path.clicked.connect(self.select_path)
        self.pushButton_select_folder.clicked.connect(self.select_folder)
        self.pushButton_open_folder.clicked.connect(self.open_folder)
        self.pushButton_rename_folder.clicked.connect(self.rename_folder)
        # 侧边栏
        self.pushButton_locate.clicked.connect(lambda: WindowLocate(self))
        self.pushButton_preview.clicked.connect(lambda: WindowPreview(self))
        self.pushButton_capture.clicked.connect(self.toggle_capture)
        self.pushButton_stitch.clicked.connect(self.start_stitch)
        self.pushButton_reclip.clicked.connect(self.start_reclip)
        # 截图设置
        self.pushButton_image_rebuild.clicked.connect(self.rebuild_images)
        self.pushButton_image_reorder.clicked.connect(self.reorder_images)
        # 拼接设置
        self.pushButton_clean_detect_data.clicked.connect(self.clean_detect_data)
        self.pushButton_manually_stitch.clicked.connect(lambda: WindowStitch(self))
        # 实时切换
        self.comboBox_log_level.currentTextChanged.connect(self.change_log_level)
        self.checkBox_always_on_top.checkStateChanged.connect(
            lambda: self.set_always_on_top(bool(self.checkBox_always_on_top.checkState().value)))

        self.init_data()

    def init_data(self) -> None:
        # 数据默认值初始化
        # file
        if getattr(sys, 'frozen', False):  # 检测程序是否处于编译环境
            _file = sys.argv[0]  # 当编译后运行时，返回exe文件的路径
        else:
            _file = os.path.abspath(__file__)  # 脚本运行时
            print(_file)
        for s in ["/", "\\", "\\\\"]:  # 初始化path，匹配三种目录表示方式
            if _file.rfind(f"{s}") >= 0:  # rfind()返回最后匹配值的索引
                self.data.exe_path = _file[:_file.rfind(f"{s}")]  # 执行文件所在目录
                self.data.ini_file = self.data.exe_path + s + "config.ini"
                self.data.score_save_path = self.data.exe_path + s + "output" + s
        # region
        self.data.region.set((int(self.frameGeometry().x()/2), int(self.frameGeometry().y()/2),
                              self.frameGeometry().width(), int(self.frameGeometry().height() / 3)))

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
        # 窗口设置
        self.set_always_on_top(self.data.always_on_top)

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
                messagebox = QMessageBox()
                messagebox.setWindowTitle(f"工作目录下已存在{self.data.score_title}文件夹")
                messagebox.setText(f"清空文件夹，或修改曲谱标题，并新建文件夹{new_title}")
                messagebox.addButton("清空文件夹", QMessageBox.ButtonRole.YesRole)
                messagebox.addButton("新建文件夹", QMessageBox.ButtonRole.NoRole)
                messagebox.addButton("取消", QMessageBox.ButtonRole.NoRole)
                messagebox.setWindowFlag(PySide6.QtCore.Qt.WindowType.WindowStaysOnTopHint, True)  # 设为置顶，必要
                messagebox.exec()
                match messagebox.clickedButton().text():
                    case "清空文件夹":
                        init_log(showlog_level=self.data.log_output_level)  # 释放进程对子日志目录的占用
                        shutil.rmtree(os.path.join(self.data.score_save_path, self.data.score_title))
                        log.success(f"已清空文件夹{self.data.score_title}")
                    case "新建文件夹":
                        self.data.score_title = new_title
                        self.flush_ui_display_data()
                        log.success(f"已新建文件夹{new_title}")
                self.flush_ui_display_data()
                return False

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
            self.capture_thread.wait()  # 等待线程结束
            self.capture_thread.exit()  # 退出线程
            self.capture_thread = CaptureThread(self.data)  # 创建新的线程，以供下次调用
            if self.pushButton_capture.text() == "结束截图":  # 保证出错时的按钮显示
                self.pushButton_capture.setText("开始截图")

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
            self.stitch_thread.wait()  # 等待线程结束
            self.stitch_thread.exit()  # 退出线程
            self.stitch_thread = StitchThread(self.data) # 创建新的线程，以供下次调用

        if self.stitch_thread.is_working:
            QMessageBox.warning(self, "警告","仍有拼接任务尚未完成，请稍后再试")
            return
        if not self.update_data_from_ui():
            return
        if self.data.score_title not in os.listdir(self.data.score_save_path):
            log.warning(
                f"未在{self.data.score_save_path}下发现{self.data.score_title}文件夹")
            return
        
        log.debug("stitich_direction:"+self.data.stitch_direction)
        log.debug("stitich_method:"+self.data.stitch_method)

        self.stitch_thread.is_working = True
        self.stitch_thread.signal_finished.connect(_finished)  # 绑定结束信号

        working_path = self.data.score_save_path + "\\" + self.data.score_title + "\\"
        self.data.working_path = working_path
        init_log(sub_log_path=working_path, showlog_level=self.data.log_output_level)  # 添加子日志

        try:
            self.stitch_thread.start()  # 启动截图线程
        except Exception:
            self.stitch_thread.signal_finished.emit()

    def start_reclip(self) -> None:
        def _finished() -> None:
            self.reclip_thread.wait()  # 等待线程结束
            self.reclip_thread.exit()  # 退出线程
            self.reclip_thread = ReclipThread(self.data)

        if self.reclip_thread.is_working:
            QMessageBox.warning(self, "警告","仍有重分割任务尚未完成，请稍后再试")
            return
        if not self.update_data_from_ui():
            return
        if self.data.score_title not in os.listdir(self.data.score_save_path):
            log.warning(f"未在{self.data.score_save_path}下发现{self.data.score_title}文件夹")
            return

        self.reclip_thread.is_working = True
        self.reclip_thread.signal_finished.connect(_finished)

        working_path = self.data.score_save_path + "\\" + self.data.score_title + "\\"
        self.data.working_path = working_path
        init_log(sub_log_path=working_path, showlog_level=self.data.log_output_level)  # 添加子日志

        try:
            self.reclip_thread.start()  # 启动截图线程
        except Exception:
            self.reclip_thread.signal_finished.emit()

    def output_log_to_ui(self, text: str) -> None:
        """
        将text打印至ui中的plain text组件
        :param text:  输出的log字符
        """
        fmt = QTextCharFormat()
        try:
            log_level = text.split("|")[1].strip()
        except IndexError:
            log_level = "ERROR"
        color = self.data.log_output_color.get(log_level)
        fmt.setForeground(QBrush(QColor(color if color else "black")))  # 文字颜色,默认黑色
        self.console.mergeCurrentCharFormat(fmt)
        self.console.append(text[:-1])  # 去除结尾的换行符
        self.console.moveCursor(QTextCursor.MoveOperation.End)  # 移动光标至末尾

    def select_path(self) -> None:
        """浏览并选择本地保存路径"""
        path = QFileDialog.getExistingDirectory(self)
        if path == "":
            return  # 当点击取消时，目录为空
        if not os.path.isdir(path) or not os.path.exists(path):
            QMessageBox.warning(self, "选择失败", "路径不合法或不存在，请重新选择",
                                QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return
        self.lineEdit_save_path.setText(path)
        self.data.score_save_path = path  # 更新数据
        os.chdir(self.data.score_save_path)  # 切换程序工作目录

    def select_folder(self) -> None:
        """浏览并选择曲谱目录"""
        if not self.update_data_from_ui():  # 更新数据:
            return
        path = QFileDialog.getExistingDirectory(self, dir=self.data.score_save_path)
        if path == "":
            return  # 当点击取消时，目录为空
        if not os.path.isdir(path) or not os.path.exists(path):
            QMessageBox.warning(self, "选择失败", "路径不合法或不存在，请重新选择",
                                QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return
        
        self.lineEdit_save_path.setText(os.path.dirname(path))  # 更新保存路径
        self.lineEdit_score_title.setText(os.path.basename(path))  # 更新曲谱标题
        self.data.score_title = self.lineEdit_score_title.text()  # 更新数据
        if os.path.isdir(path):  # 如果目录存在
            init_log(sub_log_path=self.data.score_save_path, 
                     showlog_level=self.data.log_output_level)  # 重设子日志，释放旧目录

    def open_folder(self) -> None:
        """在资源管理器中打开目录"""
        if not self.update_data_from_ui():  # 更新数据
            return
        if self.data.score_title in os.listdir(self.data.score_save_path):
            os.startfile(os.path.join(self.data.score_save_path, self.data.score_title))  # 使用startfile函数以兼容空格
        else:
            log.warning(f"打开目录失败，{self.data.score_save_path}下不存在{self.data.score_title}文件夹")

    def rename_folder(self) -> None:
        """重命名当前曲谱名及工作目录"""
        if not self.update_data_from_ui():  # 更新数据
            return
        old_title = self.data.score_title
        new_title, ok = QInputDialog.getText(self, "重命名当前曲谱工作目录及其中的文件",
                                              "请输入新的名称：", text=old_title)
        if new_title == "" or not ok:
            return
        if not is_valid_filename(new_title):
            QMessageBox.warning(self, "重命名失败", "文件名不合法",
                                QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return
        self.lineEdit_score_title.setText(new_title)  # 更新ui显示

        if os.path.isdir(os.path.join(self.data.score_save_path, old_title)):  # 重命名目录
            init_log(showlog_level=self.data.log_output_level)  # 释放旧目录的日志占用
            os.rename(os.path.join(self.data.score_save_path, old_title),
                      os.path.join(self.data.score_save_path, new_title))
            init_log(sub_log_path=os.path.join(self.data.score_save_path, new_title),
                     showlog_level=self.data.log_output_level)  # 重设子日志
            log.success(f"已将目录{old_title}重命名为{new_title}")
            for f in os.listdir(os.path.join(self.data.score_save_path, new_title)):
                if old_title in f:  # 重命名目录下,文件中的标题部分
                    os.rename(os.path.join(self.data.score_save_path, new_title, f),
                              os.path.join(self.data.score_save_path, new_title, f.replace(old_title, new_title)))
                    log.debug(f"已将文件{f}重命名为{f.replace(old_title, new_title)}")
        else:
            log.warning(f"重命名失败，{self.data.score_save_path}下不存在{old_title}文件夹，仅更新曲谱标题")
            return
        
    def rebuild_images(self) -> None:
        """从Capture图像重新构建image"""
        def _finished() -> None:
            self.buildimage_thread.wait()  # 等待线程结束
            self.buildimage_thread.exit()  # 退出线程
            self.buildimage_thread = BuildImageThread(self.data)  # 创建新的线程，以供下次调用

        if self.buildimage_thread.is_working:
            QMessageBox.warning(self, "警告", "仍有image重构建任务尚未完成，请稍后再试")
            return
        if not self.update_data_from_ui():
            return

        self.buildimage_thread.is_working = True
        self.buildimage_thread.signal_finished.connect(_finished)  # 绑定结束信号

        working_path = self.data.score_save_path + "\\" + self.data.score_title + "\\"
        self.data.working_path = working_path
        init_log(sub_log_path=working_path,
                 showlog_level=self.data.log_output_level)  # 添加子日志

        try:
            self.buildimage_thread.start()  # 启动截图线程
        except Exception:
            self.buildimage_thread.signal_finished.emit()
               
    def reorder_images(self) -> None:
        """对图像文件进行重新排序和重命名"""
        if not self.update_data_from_ui():
            return
        path = os.path.join(self.data.score_save_path, self.data.score_title)
        if not os.path.exists(path):
            log.error(f"指定路径不存在: {path}")
            return

        old_filenames = read_numbered_image_names(path, "image", order_names=False)
        ordered_filenames = order_filenames(old_filenames)

        image_format = ordered_filenames[0].split(".")[-1]
        for n in range(len(ordered_filenames)):
            ordered_filenames[n] = f"image{n}.{image_format}"

        rename_files(path, old_filenames, ordered_filenames)

    def clean_detect_data(self) -> None:
        """清除线段检测数据"""
        if not self.update_data_from_ui():
            return
        path = os.path.join(self.data.score_save_path, self.data.score_title)
        if not os.path.exists(path):
            log.error(f"指定路径不存在: {path}")
            return
        if "ScoreDetections" not in os.listdir(path):
            log.warning(f"没有找到{path}下的ScoreDetections文件")
            return
        os.remove(os.path.join(path, "ScoreDetections"))
        log.success(f"已清除{path}下的ScoreDetections文件")
        
    def set_always_on_top(self, state:bool) -> None:
        """设置窗口置顶状态"""
        # TODO 启动及切换状态时会闪一下，考虑进行优化
        self.setVisible(False)
        if state:
            self.setWindowFlag(PySide6.QtCore.Qt.WindowType.WindowStaysOnTopHint, True)
        else:
            self.setWindowFlag(PySide6.QtCore.Qt.WindowType.WindowStaysOnTopHint, False)
        self.setVisible(True)
        self.data.always_on_top = state

    def check_ui_input(self) -> bool:
        """检查ui输入数据的范围是否有效,并弹出相应的错误对话框"""
        # 目录合法检查
        if not is_valid_filename(self.lineEdit_score_title.text()):
            QMessageBox.warning(self, "曲谱标题错误", "曲谱标题不合法，请重新输入",
                                QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return False
        if not os.path.isdir(self.lineEdit_save_path.text()):
            QMessageBox.warning(self, "保存路径错误", "保存路径不合法，请重新选择",
                                QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return False
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
        self.data.always_on_top = bool(self.checkBox_always_on_top.checkState().value)
        # 定位设置
        self.data.region.set([i.value() for i in self.spinBox_region])
        # 截图设置
        if self.comboBox_compare_method.currentText() == "SSIM":
            self.data.compare_method = "SSIM"
        elif self.comboBox_compare_method.currentText() == "MSE":
            self.data.compare_method = "MSE"
        else:
            log.error(f"未识别的比较方法{self.comboBox_compare_method.currentText()}")
            return False
        self.data.compare_threshold = self.doubleSpinBox_compare_threshold.value()
        self.data.capture_delay = self.doubleSpinBox_capture_delay.value()
        self.data.if_keep_last = bool(self.checkBox_keep_last.checkState().value)
        self.data.if_reverse_image = bool(self.checkBox_reverse_image.checkState().value)
        # 拼接设置
        if self.comboBox_stitch_method.currentText() == "DIRECT":
            self.data.stitch_method = "DIRECT"
        elif self.comboBox_stitch_method.currentText() == "MSE":
            self.data.stitch_method = "MSE"
        elif self.comboBox_stitch_method.currentText() == "SSIM":
            self.data.stitch_method = "SSIM"
        else:
            log.error(f"未识别的拼接方法{self.comboBox_stitch_method.currentText()}")
            return False
        if self.radioButton_stitch_direction_horizontal.isChecked():
            self.data.stitch_direction = "horizontal"
        else:
            self.data.stitch_direction = "vertical"
        # 检测算法设置
        self.data.detect_coefficient_horizontal = self.doubleSpinBox_detect_coefficient_horizontal.value()
        self.data.detect_coefficient_vertical = self.doubleSpinBox_detect_coefficient_vertical.value()
        # # 图像识别设置
        # self.data.horizontal_lines_num = self.spinBox_horizontal_lines_num.value()
        # self.data.bar_lines_num = self.spinBox_bar_lines_num.value()
        # 重分割设置
        self.data.reclip_method = self.comboBox_reclip_method.currentIndex()
        self.data.clip_align = self.comboBox_clip_align.currentIndex()

        return True

    def flush_ui_display_data(self) -> None:
        """刷新ui显示"""
        # 全局设置
        self.lineEdit_score_title.setText(self.data.score_title)
        self.lineEdit_save_path.setText(self.data.score_save_path)
        self.comboBox_save_format.setEditText(self.data.score_save_format)
        self.comboBox_log_level.setCurrentText(self.data.log_output_level)
        self.checkBox_auto_manage_config.setChecked(self.data.if_auto_manage_config)
        self.checkBox_always_on_top.setChecked(self.data.always_on_top)
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
        # 拼接设置
        self.comboBox_stitch_method.setCurrentText(self.data.stitch_method)
        if self.data.stitch_direction == "horizontal":
            self.radioButton_stitch_direction_horizontal.setChecked(True)
            self.radioButton_stitch_direction_vertical.setChecked(False)
        elif self.data.stitch_direction == "vertical":
            self.radioButton_stitch_direction_horizontal.setChecked(False)
            self.radioButton_stitch_direction_vertical.setChecked(True)
        # 检测算法设置
        self.doubleSpinBox_detect_coefficient_horizontal.setValue(self.data.detect_coefficient_horizontal)
        self.doubleSpinBox_detect_coefficient_vertical.setValue(self.data.detect_coefficient_vertical)
        # # 图像识别设置
        # self.spinBox_horizontal_lines_num.setValue(self.data.horizontal_lines_num)
        # self.spinBox_bar_lines_num.setValue(self.data.bar_lines_num)
        # 重分割设置
        self.comboBox_reclip_method.setCurrentIndex(self.data.reclip_method)
        self.comboBox_clip_align.setCurrentIndex(self.data.clip_align)

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
        
        # 关闭其他窗口
        self.window_locate.close() if self.window_locate is not None else None
        self.window_preview.close() if self.window_preview is not None else None
        self.window_stitch.close() if self.window_stitch is not None else None

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
            self.ui.window_locate.setGeometry(
                self.data.region.region_to_geometry(  # 重设窗口位置
                without_title_frame=True))  # 减去30px标题栏高度
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
        if event is not None:
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
        self.resize(int(self.data.image_preview.shape[1] * 1.5), int(self.data.image_preview.shape[0] * 2))

        self.show()
        self.graphicsView.autoRange()  # 自动缩放图片大小

    def preview_region(self) -> None:
        """显示region区域的预览"""
        if not self.ui.update_data_from_ui():  # 检查并更新region范围
            return
        print(self.data.region)
        log.info(self.data.region.get_tuple())
        img = image_pre_process(pyautogui.screenshot(region=self.data.region.get_tuple()), self.data)
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
        img = copy.deepcopy(self.data.image_preview)
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


class WindowStitch(QWidget, Ui_Widget_Stitch):
    """
    拼接窗口，继承自QDialog，手动调整拼接点并实时显示stitched图像
    """

    def __init__(self, ui: UI):
        self.ui: UI = ui
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
        self.stitch_direction = self.data.stitch_direction
        if self.stitch_direction == "horizontal":  # 默认显示图片范围
            self.show_region = (0, int(self.viewbox.width()))  
        elif self.stitch_direction == "vertical":
            self.show_region = (0, int(self.viewbox.height()))
        log.info(f"成功加载拼接点数据，共{len(self.images)}张图片，{len(self.stitch_points)}个拼接点")
        log.debug([(n, self.stitch_points[n]) for n in range(len(self.stitch_points))])
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
            #
            self.viewbox.setAspectLocked(False)
            # 
            self.viewbox.setMouseEnabled(x=True, y=False)
            self.viewbox.setLimits(xMin=0, xMax=img.shape[1])
            # y轴自动适应缩放
            self.viewbox.enableAutoRange(axis='y', enable=True)
            self.viewbox.setAutoVisible(y=True)
            self.viewbox.setAutoPan(y=True)  # 不写这个会导致移动缩放闪烁bug
            self.viewbox.setXRange(self.show_region[0], self.show_region[1] ,padding=0)
        elif self.stitch_direction == "vertical":
            pass

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


class BuildImageThread(QtCore.QThread):
    """image构建线程"""
    signal_finished = QtCore.Signal()

    def __init__(self, data: DATA) -> None:
        super().__init__()
        self.data: DATA = data
        self.is_working: bool = False  # 主进程是否正在工作
        self.signal_stop: bool = False  # 中止线程信号

    def main(self) -> None:
        """主函数"""
        data = deepcopy(self.data)  # 深拷贝数据，避免修改原数据
        path = os.path.join(data.score_save_path, data.score_title)

        if not os.path.exists(path):
            log.error(f"指定路径不存在: {path}")
            self.signal_finished.emit()
            return

        # 获取capture图像文件名列表
        file_names = read_numbered_image_names(path, "capture")
        if file_names == []:
            self.signal_finished.emit()
            return

        # 清除旧的image文件
        image_files = read_numbered_image_names(path, "image")
        for f in image_files:
            os.remove(os.path.join(path, f))

        # 获取差异值信息
        if "CaptureData.json" in os.listdir(path):
            capture_data = CaptureData.load_from_file(
                os.path.join(path, "CaptureData.json"))
        else:
            capture_data = CaptureData()
        diff_list: list[float] = []
        captures = [read_image(os.path.join(path, f)) for f in file_names]
        for n in range(len(captures)-1):
            diff = capture_data.get_diff(
                file_names[n], file_names[n+1], data.compare_method)
            if not diff:
                diff = compare_image(cv2.cvtColor(captures[n], cv2.COLOR_RGB2GRAY),
                                     cv2.cvtColor(
                                         captures[n+1], cv2.COLOR_RGB2GRAY),
                                     method=data.compare_method)
                log.debug(
                    f"{data.compare_method}-{file_names[n]}:{file_names[n+1]}-{diff}")
                capture_data.add_diff(
                    file_names[n], file_names[n+1], data.compare_method, diff)
            diff_list.append(diff)
        capture_data.save_to_file(os.path.join(path, "CaptureData.json"))

        # 对图像取平均
        image_count = 0
        if data.compare_method == "SSIM":
            different_index = [
                n+1 for n in range(len(diff_list)) if diff_list[n] < data.compare_threshold]
        elif data.compare_method == "MSE":
            different_index = [
                n+1 for n in range(len(diff_list)) if diff_list[n] > data.compare_threshold]
        else:
            log.error(f"未知的比较方法: {data.compare_method}")
            self.signal_finished.emit()
            return
        different_index.append(0)
        if data.if_keep_last:
            different_index.append(len(diff_list)+1)  # 添加最后一组
        different_index = list(set(different_index))  # 先去重
        different_index.sort()   # 后排序
        image_names_couple = [(file_names[different_index[n]+1],
                              file_names[different_index[n+1]-2])
                              for n in range(len(different_index)-1)]
        log.debug(f"capture_index-{image_names_couple}")
        capture_sequnce = [captures[different_index[n]:different_index[n+1]]
                           for n in range(len(different_index)-1)]
        capture_sequnce = [i for i in capture_sequnce if len(i) > 2]
        image_count = 0
        for sequnce in capture_sequnce:
            image = np.average([np.asarray(i).astype(np.uint16)  # 转换为uint16，避免求和数据溢出
                                for i in sequnce[1:-1]],  # 不要首尾两张
                               axis=0  # 保留图片形状
                               ).astype(np.uint8)  # 转换回图片格式
            save_image(os.path.join(
                path, f"image{image_count}{data.score_save_format}"), image)
            image_count += 1
        log.success("image重构建完成")
        self.signal_finished.emit()

    def run(self) -> None:
        """线程入口启动函数，重写自run方法，使用.start()调用"""
        try:
            self.main()  # 调用主函数
        except Exception as e:
            log.error(f"image构建线程异常：{e}")
        finally:  # 确保线程结束时发出信号
            self.signal_finished.emit()


class CaptureThread(QtCore.QThread):
    """
    截图主线程
    """
    # 处理完毕信号
    signal_finished = QtCore.Signal()

    def __init__(self, data: DATA) -> None:
        super().__init__()
        self.data: DATA = data
        self.is_working: bool = False  # 主进程是否正在工作
        self.signal_stop: bool = False  # 中止线程信号

    def main(self) -> None:
        """截图主函数"""
        data: DATA = copy.deepcopy(self.data)  # 使用深拷贝，以保证data在执行中不变
        capture_data = CaptureData()
        temp_list: list[np.ndarray] = []
        image_list: list[np.ndarray] = []
        image_count: int = -1  # 去重后输出的单张图像数量
        temp_count: int = -1  # 每轮阈值相同的循环
        total_count: int = -1  # 总截图张数
        time.sleep(0.5)  # 略微延时
        while True:  # 图片截取主循环
            temp_list.append(image_pre_process(
                pyautogui.screenshot(region=data.region.get_tuple()), data))
            temp_count += 1
            total_count += 1
            save_image(data.working_path +
                       f"capture{total_count}{data.score_save_format}", temp_list[temp_count])
            if total_count == 0:
                log.info("===开始截图===")
            if temp_count == 0:  # 不过第一张图象不进行对比
                time.sleep(data.capture_delay)  # 延时
                continue

            # 将temp图像与上一张进行对比
            diff = compare_image(cv2.cvtColor(temp_list[temp_count], cv2.COLOR_RGB2GRAY),  # 转换为灰度图
                                 cv2.cvtColor(temp_list[temp_count - 1], cv2.COLOR_RGB2GRAY),
                                 data.compare_method)  # 指定算法
            capture_data.add_diff(  # 保存到数据类
                image1=f"capture{total_count-1}{data.score_save_format}",
                image2=f"capture{total_count}{data.score_save_format}",
                compare_method=data.compare_method,
                diff=diff)
            # 与阈值相比较
            if data.compare_method == "SSIM":
                is_different = diff < data.compare_threshold
            elif data.compare_method == "MSE":
                is_different = diff > data.compare_threshold
            else:
                log.error("未知算法类型")
                self.signal_finished.emit()
                return
            # 输出diff至log
            if is_different:
                log.info(
                    f"{data.compare_method}-{str(total_count - 1)}-{str(total_count)}={str(round(diff, 5))}")
            else:
                log.debug(
                    f"{data.compare_method}-{str(total_count - 1)}-{str(total_count)}={str(round(diff, 5))}")
                
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
                capture_data.save_to_file(data.working_path + "CaptureData.json")
                self.signal_finished.emit()
                return
            time.sleep(data.capture_delay)  # 延时


    def run(self) -> None:
        """线程入口启动函数，重写自run方法，使用.start()调用"""
        try:
            self.main()  # 调用主函数
        except Exception as e:
            log.error(f"截图线程异常：{e}")
        finally:  # 确保线程结束时发出信号
            self.signal_finished.emit() 

class StitchThread(QtCore.QThread):
    """
    图片拼接主进程
    """
    signal_finished = QtCore.Signal()  # 处理完毕信号

    def __init__(self, data: DATA):
        super().__init__()
        self.data: DATA = data
        self.is_working: bool = False  # 主进程是否正在工作

    @log.catch()
    def main(self) -> None:
        """stitch主函数"""
        data = deepcopy(self.data)
        path = data.working_path
        score_detections = ScoreDetections(path, data.score_title)
        image_files: list[str] = []

        if "ScoreDetections" in os.listdir(path):
            score_detections: ScoreDetections = ScoreDetections.load_from_file(
                os.path.join(path, "ScoreDetections"))
            image_files = score_detections.get_image_filenames()
            log.debug("成功读取缓存，跳过线段检测")
        elif data.stitch_method != "DIRECT":
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
                    image_gray = np.asarray(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY))
                    horizontal_lines = detect_horizontal_lines(image_gray, data.detect_coefficient_horizontal)
                    vertical_lines = detect_vertical_lines(image_gray, horizontal_lines, data.detect_coefficient_vertical)
                    for line in horizontal_lines:
                        line.draw(image)
                    for line in vertical_lines:
                        line.draw(image)
                    save_image(path + "\\" + filename.split(".")[0] +
                                "-detected" + data.score_save_format, image)
                    score_detections.add_image(filename, horizontal_lines, vertical_lines)
                    log.debug(
                        f"{filename}-horizontal:{len(horizontal_lines)}-vertical:{len(vertical_lines)}")
            if len(image_files) < 2:
                log.error("未发2现张或以上可供拼接的图像，请检查文件夹中image数目")
                self.signal_finished.emit()
                return
            score_detections.save_to_file(os.path.join(path, "ScoreDetections"))
            log.info("线段检测完毕，已生成对应预览图")

        # 获取排序后的图片名称
        image_names = read_numbered_image_names(path, "image")
        images = read_numbered_images(path, "image", image_names)
        images_gray:list[np.ndarray] = [np.asarray(cv2.cvtColor(i, cv2.COLOR_RGB2GRAY)) for i in images]

        # 获取mse最低时的拼接像素点
        if data.stitch_method == "DIRECT":
            log.info("直接拼接模式，跳过比对")
            stitch_points = [0] * (len(images) - 1)
        else:
            log.info("比对图片中")
            stitch_points: list[int] = []
            stitch_direction = data.stitch_direction
            # 拼接参考线方向，与拼接方向相反
            if stitch_direction == "vertical":  
                reference_lines_direction = "horizontal"
            elif stitch_direction == "horizontal":
                reference_lines_direction = "vertical"
            # 水平拼接中，获取小节数字序号的区域，以设置权重
            if stitch_direction == "horizontal":  
                barline_num_detect_start, barline_num_detect_end = get_barline_num_region(score_detections[0])
            for name_index in range(len(image_names) - 1):
                img1:np.ndarray = images_gray[name_index]
                img2:np.ndarray = images_gray[name_index + 1]
                length = img1.shape[0] if stitch_direction == "vertical" else img1.shape[1]  # 拼接方向上的长度
                try:
                    line_index = score_detections[image_names[name_index]].get_lines_index(
                        reverse=True, extern_width=2, direction=reference_lines_direction)
                    stitch_indexs = [line_index + line.start_pixel 
                                    for line in score_detections[image_names[name_index+1]].get_lines(
                                        direction=reference_lines_direction)]
                    stitch_indexs = np.unique(np.concatenate(stitch_indexs))  # 拼接成一维数组并进行去重
                    stitch_index:list[int] = list(stitch_indexs[stitch_indexs < length])  # 限定拼接索引区域范围
                except ValueError:
                    stitch_index=[]
                if stitch_index == []:  # 当img1，img2无重合特征线时
                    log.warning(f"{image_names[name_index]}与{image_names[name_index+1]}无重合特征线，"
                                "将在中间区域进行比对")
                    stitch_index = [i for i in range(1,length)]  # stitch_index不能为0!!!
                    stitch_index = stitch_index[int(length*0.2):int(length*0.8)]  # 取中间3/5的区域
                if data.stitch_method == "SSIM":
                    diff = [compare_image(clip_image(img1, stitch_direction, (-offset, None)),
                                        clip_image(img2, stitch_direction, (None, offset)),
                                        "SSIM")
                                    for offset in stitch_index if offset>7]
                    # 在水平模式中，增加小节数字序号区域的权重
                    if stitch_direction == "horizontal":
                        diff = np.asarray(diff)*0.2 + \
                            [compare_image(img1[barline_num_detect_start:barline_num_detect_end, -offset:],
                                            img2[barline_num_detect_start:barline_num_detect_end, :offset],
                                            "SSIM")*0.8
                                for offset in stitch_index if offset>7]  # SSIM算法要求最小图像大小
                    # 右侧1像素为img2的部分，越大越相似
                    stitch_points.append(int(stitch_index[np.argmax(np.asarray(diff))] + 1))
                elif data.stitch_method == "MSE":
                    img1, img2 = np.astype(img1, np.int16), np.astype(img2, np.int16)  # ！！！避免差值数据溢出
                    diff = [np.std(clip_image(img1, stitch_direction, (-offset, None)) - 
                                    clip_image(img2, stitch_direction, (None, offset)))
                            for offset in stitch_index]
                    stitch_points.append(
                        # 同上，diff越小越相似
                        int(stitch_index[np.argmin(np.asarray(diff))] + 1))
                        
                log.debug(f"{stitch_direction}:{data.stitch_method}-"
                        f"{image_names[name_index]}-{image_names[name_index + 1]}"
                        f"-stitch_point:{stitch_points[-1]}")
            log.info("图像比对完毕")

        # 保存拼接点数据
        stitchData = StitchData(stitch_points, images_gray, stitch_direction)
        stitchData.save_to_file(os.path.join(path, "StitchData.json"))

        # 进行拼接
        log.info("图像拼接中")
        final_image = stitch_images(images, stitch_points, data.stitch_direction)
        result_full_file = data.working_path+data.score_title + "-stitched" + data.score_save_format
        save_image(result_full_file, final_image)
        log.info(f"图像拼接完毕，已生成预览图{result_full_file}")

        self.signal_finished.emit()
        return

    def run(self):
        """线程入口启动函数，重写自run方法，使用.start()调用"""
        try:
            self.main()  # 调用主函数
        except Exception as e:
            log.error(f"拼接线程运行异常: {e}")
        finally:
            self.signal_finished.emit()  # 确保线程结束时发出信号


class ReclipThread(QtCore.QThread):
    """
    重分割主进程
    """

    signal_finished = QtCore.Signal()  # 处理完毕信号

    def __init__(self, data: DATA):
        super().__init__()
        self.data: DATA = data
        self.is_working: bool = False  # 主进程是否正在工作

    def main(self) -> None:
        """重分割主函数"""
        data = deepcopy(self.data)
        path = data.working_path
        stitched_image_file = data.score_title+"-stitched"+data.score_save_format
        stitched_detected_image_file = data.score_title+"-stitched-detected"+data.score_save_format
        image_path = os.path.join(path, stitched_image_file)

        if stitched_image_file not in os.listdir(path):
            log.error(f"未在当前工作目录下发现{stitched_image_file}图片，请先进行拼接操作")
            self.signal_finished.emit()
            return
        if stitched_detected_image_file in os.listdir(path):  # 移除检测过的图像
            os.remove(os.path.join(path, stitched_detected_image_file))

        # 获取检测数据
        vertical_lines: list[Line] = []
        log.info("开始检测图像中的线段")
        image = read_image(os.path.join(path, stitched_image_file))
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        if "ScoreDetections" in os.listdir(path):
            clip_length = ScoreDetections.load_from_file(
                os.path.join(path, "ScoreDetections"))[0].image_shape[1]
        else:
            clip_length = int(data.SCREEN_SIZE[0]*0.8)
        horizontal_lines, vertical_lines = detect_all_lines_with_clip(image_gray,
                                                                      clip_length,
                                                                      data.detect_coefficient_horizontal,
                                                                      data.detect_coefficient_vertical)
        for line in horizontal_lines:
            line.draw(image)
        for line in vertical_lines:
            line.draw(image)
        save_image(os.path.join(path, stitched_detected_image_file), image)
        log.debug(
            f"horizontal:{len(horizontal_lines)}-vertical:{len(vertical_lines)}")
        log.info("线段检测完毕，已生成对应预览图")

        # 小节线分组
        index = np.asarray([line.start_pixel for line in vertical_lines])
        distance = index[1:] - index[:-1]
        del_index:list[int] = []
        for i in np.where(distance < np.average(distance)/5)[0]:
            vertical_lines[i].set_thickness(
                vertical_lines[i+1].end_pixel - vertical_lines[i].start_pixel)
            del_index.append(i+1)
        bar_lines = list(np.delete(np.asarray(vertical_lines), del_index))
        image = read_image(image_path)
        image_draw = deepcopy(image)
        for line in bar_lines:
            line.draw(image_draw)
        save_image(path + "\\" + data.score_title +
                   "-detected-barlines" + data.score_save_format, image_draw)
        log.info(f"成功对小节线进行归类，共检测出{len(bar_lines)}组小节线,预览图像已保存")

        # 进行切片
        log.debug("开始进行切片操作")
        image_clips:list[np.ndarray] = []
        clip_index:list[list[int]] = []
        extern_pixel = 4  # 切片左右额外包含的像素
        if data.reclip_method == 0:  # 每行固定小节数
            each_line_bar_num = 4  # 每行的固定小节数
            for i in range(len(bar_lines)):
                if len(bar_lines) - i <= each_line_bar_num:  # 包含最后一组余数，随后跳出循环
                    clip_index.append([bar_lines[i].start_pixel - extern_pixel,
                                       bar_lines[-1].end_pixel + extern_pixel])
                    break
                elif i % each_line_bar_num == 0:
                    clip_index.append([bar_lines[i].start_pixel - extern_pixel,
                                       bar_lines[i+each_line_bar_num].end_pixel + extern_pixel])
                    if i == len(bar_lines) - 1 - each_line_bar_num:
                        break
        elif data.reclip_method == 1:  # 填充每行最大长度
            bar_lines_index = np.asarray([i.start_pixel for i in bar_lines])
            max_length = bar_lines[4].end_pixel - bar_lines[0].start_pixel  # 使用前四小节的总长度作为限制长度
            result_index = [bar_lines_index[0]]
            for i in range(bar_lines_index.size):
                if bar_lines_index[i]-result_index[-1] >= max_length:
                    # 取i-1,不超过最大长度的部分
                    result_index.append(bar_lines_index[i-1])
            result_index = np.concatenate(  # 图片索引转lines索引
                [np.where(bar_lines_index == i)[0] for i in result_index])
            if result_index[-1] != bar_lines_index.size-1:
                result_index = np.append(result_index, bar_lines_index.size-1)  # 添加入最后一组
            clip_index = [[bar_lines[result_index[i]].start_pixel - extern_pixel,
                           bar_lines[result_index[i+1]].end_pixel + extern_pixel]
                          for i in range(result_index.size-1)]
        for i in clip_index:
            clip_start = max(0, i[0])  # 确保起始位置不小于0
            clip_end = min(image.shape[1], i[1])  # 确保结束位置不大于图片宽度
            image_clips.append(image[:, clip_start:clip_end, :])  # 切片
        log.debug("成功完成切片操作")

        # 拼接
        log.debug("开始进行拼接操作")
        canvas = np.ones_like(image_clips[np.argmax(
            [c.size for c in image_clips])]).astype(np.uint8)*255  # 白色画布
        canvas = np.concatenate([canvas for _ in range(len(image_clips))], axis=0)  # 将画布的高度拓展len(clips)倍
        current_y = 0
        canvas_width = canvas.shape[1]
        for c in image_clips:
            if c.shape[1] != canvas_width:
                c:np.ndarray
                c = cv2.resize(c, (canvas_width, c.shape[0]), 
                               interpolation=cv2.INTER_CUBIC)  # 图像缩放插值方法
            h = c.shape[0]
            w = c.shape[1]
            if data.clip_align == 0:  # 靠左
                canvas[current_y:current_y+h, 0:w, :] = c
            elif data.clip_align == 1:  # 居中
                space = int((canvas_width-w)/2)
                canvas[current_y:current_y+h, space:w+space, :] = c
            elif data.clip_align == 2:  # 靠右
                canvas[current_y:current_y+h,
                       canvas_width-w:canvas_width, :] = c
            current_y += h
        save_file = path + "\\" + data.score_title + "-reclip" + data.score_save_format
        save_image(save_file, canvas)
        log.success(f"拼接操作成功完成，已成功保存图片到{save_file}")

    def run(self) -> None:
        """线程入口启动函数，重写自run方法，使用.start()调用"""
        try:
            self.main()
        except Exception as e:
            log.error(f"重分割线程运行异常：{e}")
        finally:  # 确保线程结束时发出信号
            self.signal_finished.emit()


@log.catch()
def show_main_window() -> None:
    """主窗口进程函数"""
    app = QApplication(sys.argv)
    window = UI(DATA(), app)
    window.show()
    window.activateWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    log.info("===main_start===")
    show_main_window()
    log.info("===main_finish===")
