import os
from pathlib import Path

from loguru import logger as log
from pathvalidate import is_valid_filename
from PySide6.QtWidgets import QFileDialog, QInputDialog, QMainWindow, QMessageBox

from src.Model.Data.settings import (
    buildImageSettings,
    captureSettings,
    configSettings,
    guiSettings,
    locateSettings,
    pathSettings,
    reclipSettings,
    stitchSettings,
)
from src.Model.MainTask.BuildImage import BuildImageThread
from src.Model.utils import (
    get_numbered_image_names,
    open_folder_in_explorer,
    order_filenames,
    rename_files,
    set_window_always_on_top,
)
from src.View import TabSettings_View
from src.ViewModel.binding.bind_data import bind_data


class TabSettings_VM(TabSettings_View):
    def __init__(self, main_window: QMainWindow):
        super().__init__(parent=main_window)
        self.mainWindow = main_window
        self.buildImageThread: BuildImageThread | None = None

        # Global Settings
        self.guiSettings = guiSettings
        self.pathSettings = pathSettings
        self.configSettings = configSettings
        bind_data(
            self.checkBox_always_on_top, self.guiSettings, "mainWindow_always_on_top"
        )
        bind_data(self.lineEdit_save_path, self.pathSettings, "main_out_dir")
        bind_data(
            self.lineEdit_score_title,
            self.pathSettings,
            "score_title",
            when_finished=True,
        )
        bind_data(self.checkBox_save_all_settings, self.configSettings, "auto_save_all")

        # Capture Settings
        self.buildImageSettings = buildImageSettings
        bind_data(
            self.comboBox_compare_method, self.buildImageSettings, "compare_method"
        )
        bind_data(
            self.doubleSpinBox_compare_threshold,
            self.buildImageSettings,
            "compare_threshold",
        )
        self.captureSettings = captureSettings
        bind_data(
            self.doubleSpinBox_capture_delay, self.captureSettings, "interval_time"
        )
        bind_data(self.comboBox_capture_tool, self.captureSettings, "tool")
        bind_data(self.checkBox_keep_last, self.captureSettings, "if_keep_last")
        bind_data(self.checkBox_invert_image, self.captureSettings, "if_invert_image")

        # Locate Settings
        self.locateSettings = locateSettings
        self.stitchSettings = stitchSettings
        self.reclipSettings = reclipSettings
        bind_data(self.doubleSpinBox_opacity, self.locateSettings, "window_opacity")
        bind_data(self.checkBox_auto_close, self.locateSettings, "window_auto_close")
        bind_data(self.checkBox_limit_move, self.locateSettings, "window_limit_move")
        bind_data(self.spinBox_region_x, self.locateSettings.region_data, "x")
        bind_data(self.spinBox_region_y, self.locateSettings.region_data, "y")
        bind_data(self.spinBox_region_width, self.locateSettings.region_data, "width")
        bind_data(self.spinBox_region_height, self.locateSettings.region_data, "height")
        bind_data(self.comboBox_save_format, self.captureSettings, "save_format")
        bind_data(self.comboBox_save_format, self.stitchSettings, "saving_format")
        bind_data(self.comboBox_save_format, self.reclipSettings, "saving_format")

        # Others
        bind_data(
            self.checkBox_imageViewer_show_tools,
            self.guiSettings,
            "imageViewer_show_tools",
        )
        bind_data(self.doubleSpinBox_ui_scaling, self.guiSettings, "ui_scaling")

        self.guiSettings.add_observer_handler(
            "mainWindow_always_on_top",
            lambda v: set_window_always_on_top(self.mainWindow, v),
        )

        self.pushButton_select_path.clicked.connect(self.select_main_output_dir)
        self.pushButton_select_folder.clicked.connect(self.select_score_working_folder)
        self.pushButton_open_folder.clicked.connect(self.open_folder)
        self.pushButton_rename_folder.clicked.connect(self.rename_folder)
        self.pushButton_image_reorder.clicked.connect(self.reorder_images)
        self.pushButton_image_rebuild.clicked.connect(self.rebuild_images)
        self.pushButton_clear_capture_data.clicked.connect(
            lambda: self.clear_data_file("CaptureData.json")
        )
        self.pushButton_clear_score_detections.clicked.connect(
            lambda: self.clear_data_file("ScoreDetections.json")
        )

    def select_main_output_dir(self) -> None:
        """浏览并选择本地保存路径"""
        path = QFileDialog.getExistingDirectory(self)
        if path == "":
            return  # 当点击取消时，目录为空
        self.pathSettings.main_out_dir = Path(path)

    def select_score_working_folder(self) -> None:
        """浏览并选择曲谱目录"""
        path = QFileDialog.getExistingDirectory(
            self, dir=self.pathSettings.main_out_dir.as_posix()
        )
        if path == "":
            return  # 当点击取消时，目录为空
        self.pathSettings.main_out_dir = Path(path).parent
        self.pathSettings.score_title = Path(path).name

    def open_folder(self) -> None:
        """在资源管理器中打开目录"""
        if self.pathSettings.working_dir.exists():
            open_folder_in_explorer(self.pathSettings.working_dir)
        else:
            log.warning(
                self.tr("Failed to reveal folder that does not exist: {}").format(
                    self.pathSettings.working_dir
                )
            )

    def rename_folder(self) -> None:
        """重命名当前曲谱名及工作目录"""
        old_title = self.pathSettings.score_title
        new_title, ok = QInputDialog.getText(
            self,
            self.tr("Rename Working Folder"),
            self.tr("New Folder Title:"),
            text=old_title,
        )
        if new_title == "" or not ok:
            return
        if not is_valid_filename(new_title):
            QMessageBox.warning(
                self,
                self.tr("Folder rename failed."),
                self.tr("Folder name invalid."),
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok,
            )
            return
        self.pathSettings.score_title = new_title

        old_path = self.pathSettings.main_out_dir / old_title
        new_path = self.pathSettings.main_out_dir / new_title
        if not (old_path.is_dir() and old_path.exists()):
            log.warning(
                self.tr(
                    "Folder rename failed. Working dir does not exist: {} Only switched to a new folder"
                ).format(old_path)
            )
            return
        os.chdir(self.pathSettings.main_out_dir)
        old_path.rename(new_path)
        log.success(self.tr("Renamed folder: {} -> {}").format(old_title, new_title))
        for f in new_path.iterdir():
            if old_title in f.name:  # 重命名目录下,文件中的标题部分
                new_name = f.name.replace(old_title, new_title)
                f.rename(f.parent / new_name)
                log.debug(self.tr("Renamed file: {} -> {}").format(f.name, new_name))

    def rebuild_images(self) -> None:
        """从Capture图像重新构建image"""
        if self.buildImageThread:
            QMessageBox.warning(
                self,
                self.tr("Warning"),
                self.tr(
                    "Current rebuild task is not finished, please try again later."
                ),
            )
            return
        working_dir = self.pathSettings.working_dir
        if not (
            working_dir.exists()
            and len(get_numbered_image_names(working_dir, "capture")) > 2
        ):
            QMessageBox.warning(
                self,
                self.tr("Warning"),
                self.tr("Capture images not found, please do capture first."),
            )
            return

        self.buildImageThread = BuildImageThread(
            self.buildImageSettings, self.captureSettings, working_dir
        )
        self.buildImageThread.destroyed.connect(
            lambda: setattr(self, "buildImageThread", None)
        )
        self.buildImageThread.start()  # 启动截图线程

    def reorder_images(self) -> None:
        """对图像文件进行重新排序和重命名"""
        path = self.pathSettings.working_dir
        if not path.exists():
            log.error(self.tr("Path does not exist: {}").format(path))
            return

        old_filenames = get_numbered_image_names(path, "image")
        ordered_filenames = order_filenames(old_filenames)

        image_format = ordered_filenames[0].split(".")[-1]
        for n in range(len(ordered_filenames)):
            ordered_filenames[n] = f"image{n}.{image_format}"

        rename_files(path, old_filenames, ordered_filenames)

    def clear_data_file(self, filename: str) -> None:
        if (path := self.pathSettings.working_dir / filename).exists():
            os.remove(path)
            log.info(self.tr("{} Removed: {}").format(filename.split(".")[0], path))
        else:
            log.info(self.tr("File not found: {}").format(path))
