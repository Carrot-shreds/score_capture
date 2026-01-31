import os
import shutil

from loguru import logger as log
from PySide6 import QtCore
from PySide6.QtCore import QSettings
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMessageBox

from src import __version__
from src.Model.Data.settings import (
    appSettings,
    appSettingsSavingConfig,
)
from src.Model.MainTask.Capture import CaptureThread
from src.Model.utils import get_unused_filename
from src.View import MainWindow_View
from src.ViewModel import (
    DialogLocate_VM,
    TabConsole_VM,
    TabPreview_VM,
    TabReclip_VM,
    TabSettings_VM,
    TabStitch_VM,
)
from src.ViewModel.binding.bind_data import bind_data


class MainWindow_VM(MainWindow_View):
    def __init__(self) -> None:
        super().__init__()
        # settings
        self.appSettings = appSettings
        self.appSettingsSavingConfig = appSettingsSavingConfig
        self.guiSettings = self.appSettings.gui_settings
        self.pathSettings = self.appSettings.path_settings
        self.captureSettings = self.appSettings.capture_settings
        self.locateSettings = self.appSettings.locate_settings
        self.previewSetting = self.appSettings.preview_settings
        self.buildImageSettings = self.appSettings.build_image_settings
        self.captureThread: CaptureThread | None = None
        self.dockSettings = QSettings(
            (self.pathSettings.config_dir / "dockSettings.ini").as_posix(),
            QSettings.Format.IniFormat,
        )

        # tabs
        self.tab_console = TabConsole_VM(self)
        self.tab_settings = TabSettings_VM(self)
        self.tab_preview = TabPreview_VM(self)
        self.tab_stitch = TabStitch_VM(self)
        self.tab_reclip = TabReclip_VM(self)
        self.create_docking_system(
            tab_console=self.tab_console,
            tab_settings=self.tab_settings,
            tab_preview=self.tab_preview,
            tab_stitch=self.tab_stitch,
            tab_reclip=self.tab_reclip,
        )
        self.dialog_locate = DialogLocate_VM(self)

        # tool bar
        bind_data(self.lineEdit_score_title, self.pathSettings, "score_title")
        bind_data(
            self.perspective_combobox, self.guiSettings, "mainWindow_dock_perspective"
        )
        self.action_locate.triggered.connect(self.dialog_locate.show)
        self.action_preview.triggered.connect(self.tab_preview.preview_region)
        self.action_stitch.triggered.connect(self.tab_stitch.start_stitch)
        self.action_select_folder.triggered.connect(
            self.tab_settings.select_score_working_folder
        )
        self.action_open_folder.triggered.connect(self.tab_settings.open_folder)
        self.action_capture.toggled.connect(self.toggle_capture)

        # state bar
        self.label_version.setText("V" + __version__)
        self.pathSettings.add_observer_handlers(
            ["main_out_dir", "score_title"],
            lambda v: self.label_working_dir.setText(
                self.pathSettings.working_dir.as_posix()
            ),
        )

        self.dialog_locate.pushButton_preview.clicked.connect(
            self.tab_preview.preview_region
        )

        self.load_dock_perspective()
        self.appSettings.notice_all_observers()

    def load_dock_perspective(self) -> None:
        self.dock_manager.loadPerspectives(self.dockSettings)
        if "default" not in self.dock_manager.perspectiveNames():
            self.new_docking_perspective("default")
        self.perspective_combobox.blockSignals(True)
        self.perspective_combobox.clear()
        self.perspective_combobox.addItems(self.dock_manager.perspectiveNames())
        self.perspective_combobox.blockSignals(False)
        if (
            self.guiSettings.mainWindow_dock_perspective
            not in self.dock_manager.perspectiveNames()
        ):
            self.guiSettings.mainWindow_dock_perspective = "default"
        self.perspective_combobox.setCurrentText(
            self.guiSettings.mainWindow_dock_perspective
        )
        self.dock_manager.openPerspective(self.guiSettings.mainWindow_dock_perspective)

    def toggle_capture(self, state: bool) -> None:
        """切换截图开始状态"""
        if not state:
            if not self.captureThread:
                return
            self.action_capture.setDisabled(True)  # 暂时禁用按钮
            self.captureThread.stop_flag.set(True)  # 发送停止信号
            return

        if self.captureThread:
            log.warning("当前截图任务仍未结束，请稍后重试")
            self.action_capture.setChecked(False)
            return

        if self.pathSettings.working_dir.exists():  # 解决文件夹重名问题
            new_title = get_unused_filename(
                self.pathSettings.score_title, self.pathSettings.main_out_dir
            )
            messagebox = QMessageBox()
            messagebox.setWindowTitle(
                f"工作目录下已存在{self.pathSettings.score_title}文件夹"
            )
            messagebox.setText(f"清空文件夹，或修改曲谱标题，并新建文件夹{new_title}")
            messagebox.addButton("清空文件夹", QMessageBox.ButtonRole.YesRole)
            messagebox.addButton("新建文件夹", QMessageBox.ButtonRole.NoRole)
            messagebox.addButton("取消", QMessageBox.ButtonRole.NoRole)
            messagebox.setWindowFlag(
                QtCore.Qt.WindowType.WindowStaysOnTopHint, True
            )  # 设为置顶，必要
            messagebox.exec()
            match messagebox.clickedButton().text():
                case "清空文件夹":
                    os.chdir(self.pathSettings.main_out_dir)  # release old dir
                    shutil.rmtree(self.pathSettings.working_dir)
                    log.success(f"已清空文件夹{self.pathSettings.score_title}")
                case "新建文件夹":
                    self.pathSettings.score_title = new_title
                    log.success(f"已切换到新文件夹{self.pathSettings.score_title}")
            self.action_capture.setChecked(False)
            return  # break out

        self.pathSettings.working_dir.mkdir()
        self.captureThread = CaptureThread(
            self.captureSettings,
            self.buildImageSettings,
            self.locateSettings.region_data,
            self.pathSettings.working_dir,
        )
        self.captureThread.signalBuildImage.connect(
            lambda path: self.tab_preview.open_image(path)
            if self.previewSetting.live_preview
            else None
        )
        self.captureThread.finished.connect(
            lambda: self.action_capture.setDisabled(False)
        )  # 复位按钮状态
        self.captureThread.destroyed.connect(
            lambda: setattr(self, "captureThread", None)
        )
        self.captureThread.start()  # 启动截图线程

    def closeEvent(self, event: QCloseEvent):
        self.dialog_locate.close()
        self.tab_reclip.close()  # To emit tab's close event

        self.dock_manager.savePerspectives(self.dockSettings)
        self.dockSettings.sync()
        self.appSettingsSavingConfig.save()
        self.appSettings.save()
        super().closeEvent(event)
