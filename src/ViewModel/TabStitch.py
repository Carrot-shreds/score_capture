import gc
import time
from pathlib import Path
from typing import Self

import cv2
import numpy as np
from loguru import logger as log
from pydantic import ConfigDict, ValidationError, model_validator
from pyqtgraph import ViewBox
from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QFileDialog

from src.Model.Data.const import Direction
from src.Model.Data.data import ScoreStitchData
from src.Model.Data.settings import (
    guiSettings,
    lineDetectorSettings,
    pathSettings,
    shortcutSettings,
    stitchSettings,
)
from src.Model.Data.type import (
    AlwaysValidateModel,
    DirectoryExisting,
    ImageArray,
    ImageFileName,
    JsonPath,
    OnValueChangeModel,
)
from src.Model.image_process import stitch_images
from src.Model.MainTask.Stitch import StitchThread
from src.Model.utils import (
    get_numbered_image_names,
    read_images,
    save_image,
)
from src.View import TabStitch_View
from src.View.widgets.ImageViewer import ImageViewer
from src.ViewModel.binding.bind_data import bind_data


class ManualStitchData(AlwaysValidateModel, OnValueChangeModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    score_stitch_data: ScoreStitchData
    imageViewer: ImageViewer
    stitch_points: list[int] = [0]
    current_index: int = 0
    working_dir: DirectoryExisting
    image_names: list[ImageFileName]
    image_origins: list[ImageArray]
    image_stitched: ImageArray

    def __init__(self, stitch_data_path: JsonPath, imageviewer: ImageViewer) -> None:
        score_stitch_data = ScoreStitchData.load_from_file(stitch_data_path)
        stitch_points = score_stitch_data.stitch_points
        working_dir = stitch_data_path.parent
        image_names = get_numbered_image_names(working_dir, "image")
        image_origins = read_images(working_dir, image_names)
        image_stitched = stitch_images(
            image_origins, stitch_points, score_stitch_data.stitch_settings.direction
        )
        super().__init__(
            score_stitch_data=score_stitch_data,
            imageViewer=imageviewer,
            stitch_points=stitch_points,
            working_dir=working_dir,
            image_names=image_names,
            image_origins=image_origins,
            image_stitched=image_stitched,
        )
        self.add_observer_handler("current_index", lambda v: self.set_view_region())

    @property
    def image_shapes(self) -> list[tuple[int, int]]:
        return self.score_stitch_data.image_shapes

    @property
    def current_point(self) -> int:
        return self.stitch_points[self.current_index]

    @current_point.setter
    def current_point(self, value: int) -> None:
        self.stitch_points[self.current_index] = value

    @property
    def direction(self) -> Direction:
        return self.score_stitch_data.stitch_settings.direction

    @property
    def stitched_image_length(self) -> int:
        return self.image_stitched.shape[self.direction]

    @property
    def viewbox_length(self) -> int:
        viewbox = self.imageViewer.imageView.getView()
        match self.direction:
            case Direction.HORIZONTAL:
                return int(viewbox.width())
            case Direction.VERTICAL:
                return int(viewbox.height())

    @property
    def display_region(self) -> tuple[int, int]:
        viewbox_length = self.viewbox_length
        stitched_image_length = self.stitched_image_length
        point_position: int = self.image_length(0) + sum(
            [
                self.image_length(i) - self.stitch_points[i]
                for i in range(self.current_index)
            ]
        )
        blank = int(viewbox_length / 2)
        if point_position + blank > stitched_image_length - 1:
            return (
                stitched_image_length - 1 - viewbox_length,
                stitched_image_length - 1,
            )
        else:
            return (point_position - blank, point_position + blank)

    def build_score_stitch_data(self) -> ScoreStitchData:
        data = self.score_stitch_data.data
        [
            setattr(data[i], "stitch_point", self.stitch_points[i])
            for i in range(len(self.stitch_points))
        ]
        new_data = self.score_stitch_data.model_copy(deep=True)
        new_data.data = data
        return new_data

    def update_image_stitched(self) -> None:
        self.image_stitched = stitch_images(
            self.image_origins, self.stitch_points, self.direction
        )

    def image_length(self, index: int, direction: Direction | None = None) -> int:
        "default on the stitch direction"
        if not direction:
            direction = self.score_stitch_data.stitch_settings.direction
        return self.image_shapes[index][direction]

    def lock_view_zoom(self, viewbox: ViewBox | None = None):
        viewbox = self.imageViewer.imageView.getView() if viewbox is None else viewbox
        "设置显示样式和范围"
        if self.direction == Direction.HORIZONTAL:
            # 关闭缩放锁定
            viewbox.setAspectLocked(False)
            # 仅允许x轴缩放
            viewbox.setMouseEnabled(x=True, y=False)
            viewbox.setLimits(xMin=0, xMax=self.stitched_image_length)
            # y轴自动适应缩放
            viewbox.enableAutoRange(axis="y", enable=True)
            viewbox.setAutoVisible(y=True)
            viewbox.setAutoPan(y=True)  # 不写这个会导致移动缩放闪烁bug
        elif self.direction == Direction.VERTICAL:
            # 关闭缩放锁定
            viewbox.setAspectLocked(False)
            # 仅允许y轴缩放
            viewbox.setMouseEnabled(x=False, y=True)
            viewbox.setLimits(yMin=0, yMax=self.stitched_image_length)
            # x轴自动适应缩放
            viewbox.enableAutoRange(axis="x", enable=True)
            viewbox.setAutoVisible(x=True)
            viewbox.setAutoPan(x=True)  # 不写这个会导致移动缩放闪烁bug

    def unlock_view_zoom(self, viewbox: ViewBox | None = None):
        viewbox = self.imageViewer.imageView.getView() if viewbox is None else viewbox
        # defalut value of state in ViewBox.__init__()
        viewbox.setMouseEnabled(x=True, y=True)
        viewbox.setLimits(xMin=-1e307, xMax=+1e307, yMin=-1e307, yMax=+1e307)
        viewbox.enableAutoRange(axis="x", enable=True)
        viewbox.enableAutoRange(axis="y", enable=True)
        viewbox.setAutoVisible(x=False, y=False)
        viewbox.setAutoPan(x=False, y=False)

    def toggle_view_zoom_lock(self, state: bool):
        if state:
            self.lock_view_zoom()
        else:
            self.unlock_view_zoom()
        self.set_view_region()

    def set_view_region(self):
        viewbox = self.imageViewer.imageView.getView()
        region = self.display_region
        "设置显示样式和范围"
        if self.direction == Direction.HORIZONTAL:
            viewbox.setXRange(region[0], region[1], padding=0)
        elif self.direction == Direction.VERTICAL:
            viewbox.setYRange(region[0], region[1], padding=0)

    @model_validator(mode="after")
    def validator(self) -> Self:
        if self.stitch_points == []:
            raise ValueError("Stitch points can not be empty")
        if self.image_names == []:
            raise ValueError(f"{self.working_dir}下未发现image文件")
        if self.current_index < 0 or self.current_index > len(self.stitch_points) - 1:
            raise ValueError(
                f"current index{self.current_index} not in the correct region:0-{len(self.stitch_points) - 1}"
            )
        length_bound = self.image_length(self.current_index + 1)
        if self.current_point < 0 or self.current_point > length_bound:
            raise ValueError(
                f"current stitch point:{self.current_point} out off bound of image, must in 0-{length_bound}"
            )
        return self


class TabStitch_VM(TabStitch_View):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainWindow = parent
        self.viewbox = self.ImageViewer.imageView.getView()
        self.stitchThread: StitchThread | None = None
        self.manualStitchData: ManualStitchData | None = None
        self.working_stitchData_path: Path | None = None

        self.pathSettings = pathSettings
        self.stitchSettings = stitchSettings
        self.detectorSettings = lineDetectorSettings
        self.shortcutSettings = shortcutSettings

        bind_data(self.comboBox_stitch_method, self.stitchSettings, "method")
        bind_data(
            self.radioButton_stitch_direction_horizontal,
            self.stitchSettings,
            "direction",
        )
        bind_data(self.checkBox_lock_zoom, self.stitchSettings, "ui_lock_zoom")
        bind_data(self.checkBox_show_mark_point, self.stitchSettings, "add_mark_point")
        bind_data(
            self.doubleSpinBox_location_mark_point,
            self.stitchSettings,
            "location_mark_point",
        )

        guiSettings.add_observer_handler(
            "imageViewer_show_tools", self.ImageViewer.toggle_tools
        )
        self.pathSettings.add_observer_handlers(
            ["main_out_dir", "score_title"], lambda v: self.handle_working_dir_changed()
        )
        self.stitchSettings.add_observer_handler(
            "ui_lock_zoom",
            lambda v: (
                self.manualStitchData.toggle_view_zoom_lock(v)
                if self.manualStitchData
                else None
            ),
        )

        self.pushButton_start_stitiching.clicked.connect(self.start_stitch)
        self.pushButton_select_file.clicked.connect(self.handel_select_stitch_data_file)
        self.pushButton_save_file.clicked.connect(self.handel_save_stitch_data_file)
        self.pushButton_save_file_as.clicked.connect(
            self.handel_save_sttich_data_file_as
        )
        self.pushButton_save_image.clicked.connect(self.handel_save_stitched_image)

        shortcut_save = QShortcut(self.tab_manual)
        shortcut_save.setKey(QKeySequence.StandardKey.Save)
        shortcut_save.activated.connect(
            lambda: [
                self.handel_save_stitch_data_file(),
                self.handel_save_stitched_image(),
            ]
        )
        self.pushButton_save_file_as.setShortcut(QKeySequence.StandardKey.SaveAs)
        self.tabWidget.setShortcutEnabled(True)

    def keyPressEvent(self, ev: QtGui.QKeyEvent, /) -> None:
        super().keyPressEvent(ev)
        modifiers = ev.modifiers()

        if (
            Qt.Key.Key_1 <= ev.key() <= Qt.Key.Key_9
            and 0 <= (index := (int(ev.text()) - 1)) <= self.tabWidget.count()
        ):
            self.tabWidget.setCurrentIndex(index)

        if not self.manualStitchData:
            return
        try:
            max_index = len(self.manualStitchData.stitch_points) - 1
            max_point = self.manualStitchData.image_length(
                self.manualStitchData.current_index + 1
            )
            match ev.key():
                case self.shortcutSettings.manualStitch_key_prev_index:
                    step = self.shortcutSettings.get_move_step("index", modifiers)
                    if (self.manualStitchData.current_index - step) >= 0:
                        self.manualStitchData.current_index -= step
                    else:
                        self.manualStitchData.current_index = 0
                case self.shortcutSettings.manualStitch_key_next_index:
                    step = self.shortcutSettings.get_move_step("index", modifiers)
                    if self.manualStitchData.current_index < (max_index - step):
                        self.manualStitchData.current_index += step
                    else:
                        self.manualStitchData.current_index = max_index
                case self.shortcutSettings.manualStitch_key_add_point:
                    step = self.shortcutSettings.get_move_step("point", modifiers)
                    if self.manualStitchData.current_point < max_point:
                        self.manualStitchData.current_point += step
                    else:
                        self.manualStitchData.current_point = max_point
                case self.shortcutSettings.manualStitch_key_sub_point:
                    step = self.shortcutSettings.get_move_step("point", modifiers)
                    if (self.manualStitchData.current_point - step) >= 0:
                        self.manualStitchData.current_point -= step
                    else:
                        self.manualStitchData.current_point = 0
                case self.shortcutSettings.manualStitch_key_min_index:
                    self.manualStitchData.current_index = 0
                case self.shortcutSettings.manualStitch_key_max_index:
                    self.manualStitchData.current_index = max_index
                case self.shortcutSettings.manualStitch_key_min_point:
                    self.manualStitchData.current_point = 0
                case self.shortcutSettings.manualStitch_key_max_point:
                    self.manualStitchData.current_point = max_point
        except ValidationError:
            return

    def load_stitch_data(self, file: JsonPath) -> bool:
        if not file.exists():
            log.error(f"ScoreStitchData Not Found:{file}")
            return False
        if file.parent != self.pathSettings.working_dir:
            self.pathSettings.working_dir = file.parent

        # disconnect all slot, to prevent repeat connect
        if self.manualStitchData:  # TODO weakref auto release
            self.spinBox_stitch_points_index.valueChanged.disconnect()
            self.spinBox_stitch_points_value.valueChanged.disconnect()

        self.manualStitchData = ManualStitchData(file, self.ImageViewer)
        self.spinBox_stitch_points_index.setMaximum(
            len(self.manualStitchData.stitch_points) - 1
        )
        self.spinBox_stitch_points_value.setMaximum(
            self.manualStitchData.image_length(1)
        )
        bind_data(
            self.spinBox_stitch_points_index, self.manualStitchData, "current_index"
        )
        bind_data(
            self.spinBox_stitch_points_value, self.manualStitchData, "current_point"
        )
        self.manualStitchData.add_observer_handler(
            "current_index", self.handle_point_index_changed
        )
        self.manualStitchData.add_observer_handler(
            "current_point", self.handle_point_value_changed
        )

        self.ImageViewer.imageView.clear()  # clear screen,then flush_stitch_image will do autoHistogramRange using setImage()
        self.ImageViewer.set_label_text(
            self.manualStitchData.working_dir.name + " Stitched Preview"
        )
        self.working_stitchData_path = file
        log.success(f"Loaded {file}")
        gc.collect()  # Necessary, solve the memory leak

        return True

    def handel_select_stitch_data_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            dir=self.pathSettings.working_dir.as_posix(),
            filter="ScoreStitchData (ScoreStitchData*.json)",
        )
        if path == "":
            return
        self.load_stitch_data(Path(path))
        self.flush_stitch_preview()

    def handel_load_current_folder_stitch_data_file(self) -> None:
        if not (
            file := self.pathSettings.working_dir / "ScoreStitchData.json"
        ).exists():
            return
        self.load_stitch_data(file)
        self.flush_stitch_preview()

    def handel_save_stitch_data_file(self) -> None:
        if not self.manualStitchData or not self.working_stitchData_path:
            return
        self.manualStitchData.build_score_stitch_data().save_to_file(
            self.working_stitchData_path
        )
        log.success(f"已保存拼接点数据至{self.working_stitchData_path}")

    def handel_save_sttich_data_file_as(self) -> None:
        name = f"ScoreStitchData_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json"
        file, _ = QFileDialog.getSaveFileName(
            dir=(self.pathSettings.working_dir / name).as_posix(),
            filter="ScoreStitchData (*.json)",
        )
        if file == "" or not self.manualStitchData:
            return
        self.manualStitchData.build_score_stitch_data().save_to_file(Path(file))
        log.success(f"已保存拼接点数据至{file}")

    def handel_save_stitched_image(self) -> None:
        if not self.manualStitchData:
            return
        name = f"{self.pathSettings.score_title}-stitched{self.stitchSettings.saving_format}"
        save_image(
            self.pathSettings.working_dir / name, self.manualStitchData.image_stitched
        )
        log.success(f"已保存拼接预览图像至{self.pathSettings.working_dir / name}")

    def handle_point_index_changed(self, index: int) -> None:
        if not self.manualStitchData:
            return
        self.spinBox_stitch_points_value.setMaximum(
            self.manualStitchData.image_length(index + 1)
        )
        self.spinBox_stitch_points_value.setValue(
            self.manualStitchData.stitch_points[index]
        )

    def handle_point_value_changed(self, _: int) -> None:
        if not self.manualStitchData:
            return
        self.manualStitchData.update_image_stitched()
        self.flush_stitch_preview()

    def handle_working_dir_changed(self) -> None:
        if (
            self.manualStitchData is not None
            and self.manualStitchData.working_dir == self.pathSettings.working_dir
        ):
            return
        if (self.pathSettings.working_dir / "ScoreStitchData.json").exists():
            self.handel_load_current_folder_stitch_data_file()
        else:
            self.manualStitchData = None
            self.ImageViewer.clear()

    def flush_stitch_preview(self):
        if not self.manualStitchData:
            self.load_stitch_data(
                self.pathSettings.working_dir / "ScoreStitchData.json"
            )
        if not self.manualStitchData:
            return

        image = self.manualStitchData.image_stitched
        if self.stitchSettings.add_mark_point:
            if self.manualStitchData.direction == Direction.HORIZONTAL:
                point = (
                    int(np.average(self.manualStitchData.display_region)),
                    int(image.shape[0] * self.stitchSettings.location_mark_point),
                )
            else:
                point = (
                    int(image.shape[1] * self.stitchSettings.location_mark_point),
                    int(np.average(self.manualStitchData.display_region)),
                )
            cv2.circle(image, point, 4, (0, 0, 255), -1)

        if self.ImageViewer.current_image is None:  # after load score stitch file
            self.ImageViewer.imageView.setImage(image, autoRange=False)
            self.manualStitchData.toggle_view_zoom_lock(
                self.stitchSettings.ui_lock_zoom
            )
        else:
            self.ImageViewer.imageView.imageItem.updateImage(image)
        self.manualStitchData.set_view_region()

    def start_stitch(self) -> None:
        if self.stitchThread:
            log.warning("当前拼接任务仍未结束，请稍后重试")
            return
        if not self.pathSettings.working_dir.exists():
            log.warning(f"当前工作目录{self.pathSettings.working_dir}不存在")
            return

        self.stitchThread = StitchThread(
            self.stitchSettings,
            self.detectorSettings,
            self.pathSettings.working_dir,
        )
        self.stitchThread.finished.connect(self.flush_stitch_preview)
        self.stitchThread.destroyed.connect(lambda: setattr(self, "stitchThread", None))
        self.stitchThread.start()
