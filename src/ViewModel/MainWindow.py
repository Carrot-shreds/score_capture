import os
import shutil
import sys
from pathlib import Path

from loguru import logger as log
from PySide6 import QtCore
from PySide6.QtCore import QProcess, QSettings
from PySide6.QtGui import QAction, QCloseEvent
from PySide6.QtWidgets import QApplication, QMessageBox

from src import __version__
from src.Model.Data.settings import (
    appSettings,
    appSettingsSavingConfig,
)
from src.Model.MainTask.Capture import CaptureThread
from src.Model.utils import get_unused_filename
from src.View import MainWindow_View
from src.View.MainWindow import About
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

        self.dock_widget_stitch.visibilityChanged.connect(
            lambda state:  # When tab is not visable, viewbox.height() will get wrong 30px value.
            self.tab_stitch.reset_region() if state else None
        )

        # tool bar
        bind_data(
            self.lineEdit_score_title,
            self.pathSettings,
            "score_title",
            when_finished=True,
        )
        bind_data(
            self.perspective_combobox, self.guiSettings, "mainWindow_dock_perspective"
        )
        bind_data(
            self.action_mainwindow_always_top,
            self.guiSettings,
            "mainWindow_always_on_top",
        )

        # Actions
        self.action_locate.triggered.connect(self.dialog_locate.show)
        self.action_preview.triggered.connect(self.tab_preview.preview_region)
        self.action_stitch.triggered.connect(self.tab_stitch.start_stitch)
        self.action_reclip.triggered.connect(self.tab_reclip.start_reclip)
        self.action_print_score.triggered.connect(self.tab_reclip.printing_preview)
        self.action_output_pdf.triggered.connect(self.tab_reclip.save_pdf)
        self.action_select_folder.triggered.connect(
            self.tab_settings.select_score_working_folder
        )
        self.action_open_folder.triggered.connect(self.tab_settings.open_folder)
        self.action_capture.toggled.connect(self.toggle_capture)
        self.dialog_locate.pushButton_toggle_capture.clicked.connect(
            self.action_capture.toggle
        )
        self.action_rename_folder.triggered.connect(self.tab_settings.rename_folder)
        self.action_about.triggered.connect(lambda: About(self, __version__))
        self.add_language_switch()

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
        self.toolBar_path.setFocus()
        self.appSettings.notice_all_observers()

    def add_language_switch(self) -> None:
        from src.View.MainWindow import LANGUAGES

        actions: list[QAction] = []

        def handel(action: QAction):
            for a in actions:
                a.blockSignals(True)
                a.setEnabled(True)
                a.setChecked(False)
                a.blockSignals(False)
            action.blockSignals(True)
            action.setChecked(True)
            action.setEnabled(False)
            action.blockSignals(False)
            lang = LANGUAGES[action.text()]
            self.guiSettings.language = lang

            # restart
            self.close()
            p = QProcess
            app = QApplication.instance()
            if not app:
                return
            exe = app.applicationFilePath()
            if Path(exe).name.find("python") >= 0:
                p.startDetached(
                    sys.executable,
                    [(Path(__file__).parent.parent.parent / "main.py").as_posix()],
                )
            else:
                p.startDetached(exe)

        for k, v in LANGUAGES.items():
            action = QAction(self)
            action.setText(k)
            action.setCheckable(True)
            if self.guiSettings.language == v:
                action.setChecked(True)
                action.setEnabled(False)
            action.toggled.connect(lambda state, a=action: handel(a) if state else None)
            self.menuLanguage.addAction(action)
            actions.append(action)

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
            self.dialog_locate.pushButton_toggle_capture.setDisabled(True)
            self.captureThread.stop_flag.set(True)  # 发送停止信号
            return

        if self.captureThread:
            log.warning(
                self.tr("Current capture task is not finished. Please try again later.")
            )
            self.action_capture.setChecked(False)
            return

        if self.pathSettings.working_dir.exists():  # 解决文件夹重名问题
            new_title = get_unused_filename(
                self.pathSettings.score_title, self.pathSettings.main_out_dir
            )
            messagebox = QMessageBox()
            messagebox.setWindowTitle(
                self.tr("Working folder is not empty: {}").format(
                    self.pathSettings.score_title
                )
            )
            text_clear_folder = self.tr("Clear folder")
            text_new_folder = self.tr("New folder")
            messagebox.setText(
                self.tr(
                    "Clear current folder, or switch to a new folder named: {}"
                ).format(new_title)
            )
            messagebox.addButton(text_clear_folder, QMessageBox.ButtonRole.YesRole)
            messagebox.addButton(text_new_folder, QMessageBox.ButtonRole.NoRole)
            messagebox.addButton(self.tr("Cancel"), QMessageBox.ButtonRole.NoRole)
            messagebox.setWindowFlag(
                QtCore.Qt.WindowType.WindowStaysOnTopHint, True
            )  # 设为置顶，必要
            messagebox.exec()
            result_text = messagebox.clickedButton().text()
            if result_text == text_clear_folder:
                os.chdir(self.pathSettings.main_out_dir)  # release old dir
                shutil.rmtree(self.pathSettings.working_dir)
                log.success(
                    self.tr("Folder cleared: {}").format(self.pathSettings.score_title)
                )
            elif result_text == text_new_folder:
                self.pathSettings.score_title = new_title
                log.success(
                    self.tr("Switched to new folder: {}").format(
                        self.pathSettings.score_title
                    )
                )
            self.action_capture.setChecked(False)
            return  # break out

        if not self.pathSettings.main_out_dir.exists():
            self.pathSettings.main_out_dir.mkdir()
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
        self.captureThread.signalBuildImage.connect(
            lambda path: self.dialog_locate.flash_capture_button(200, "lightgreen")
        )
        self.captureThread.signalCaptured.connect(
            lambda path: self.dialog_locate.flash_capture_button(200, "lightblue")
        )

        self.captureThread.finished.connect(
            lambda: [
                self.action_capture.setDisabled(False),
                self.dialog_locate.pushButton_toggle_capture.setDisabled(False),
                self.dialog_locate.pushButton_toggle_capture.setText("📷"),
            ]
        )  # 复位按钮状态
        self.captureThread.destroyed.connect(
            lambda: setattr(self, "captureThread", None)
        )

        self.captureThread.start()  # 启动截图线程
        self.dialog_locate.pushButton_toggle_capture.setText("📸")

    def closeEvent(self, event: QCloseEvent):
        self.dialog_locate.close()
        self.tab_reclip.close()  # To emit tab's close event

        self.dock_manager.savePerspectives(self.dockSettings)
        self.dockSettings.sync()
        self.appSettingsSavingConfig.save()
        self.appSettings.save()
        super().closeEvent(event)
