import os
import sys
import shutil
import subprocess
from typing import Optional

import mss
from loguru import logger as log
import PySide6.QtCore
from PySide6.QtGui import QCloseEvent, QColor, QTextCursor, QTextCharFormat, QBrush
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QInputDialog

from view.mainwindow_ui import Ui_MainWindow
from .WindowLocate import WindowLocate
from .WindowPreview import WindowPreview
from .WindowStitch import WindowStitch

from Model.MainTask.BuildImage import BuildImageThread
from Model.MainTask.Capture import CaptureThread
from Model.MainTask.Stitch import StitchThread
from Model.MainTask.Reclip import ReclipThread

from Model.data import DATA
from Model.log import LogThread, init_log
from Model.utils import is_valid_filename, order_filenames, read_numbered_image_names, open_folder_in_explorer, rename_files

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
        
        # screen
        with mss.mss() as sct:
            monitors = sct.monitors
            if self.data.monitor_num < 1 or self.data.monitor_num >= len(monitors):
                log.error(f"无效的显示器编号: {self.data.monitor_num}, 使用默认显示器1")
                self.data.monitor_num = 1
            self.data.SCREEN_SIZE = (monitors[self.data.monitor_num]['width'],
                monitors[self.data.monitor_num]['height'])

        # capture tool
        if os.environ.get("XDG_SESSION_TYPE") == "wayland":
            if os.environ.get("XDG_SESSION_DESKTOP") == "KDE":
                self.data.capture_tool = "spectacle"
            # 使用command -v检查命令是否存在
            elif subprocess.run(["command -v grim"], shell=True, capture_output=True).stdout:
                self.data.capture_tool = "grim"
        else:
            self.data.capture_tool = "mss"

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

            working_path = os.path.join(self.data.score_save_path, self.data.score_title)
            os.mkdir(working_path)
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

        working_path = os.path.join(self.data.score_save_path, self.data.score_title)
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

        working_path = os.path.join(self.data.score_save_path, self.data.score_title)
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
            open_folder_in_explorer(os.path.join(self.data.score_save_path, self.data.score_title))
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

        working_path = os.path.join(self.data.score_save_path, self.data.score_title)
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
        self.data.capture_tool = self.comboBox_capture_tool.currentText()
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
        self.comboBox_capture_tool.setCurrentText(self.data.capture_tool)
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

