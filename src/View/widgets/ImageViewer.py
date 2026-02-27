from pathlib import Path
from typing import Literal, TypedDict

import numpy as np
import pyqtgraph
from pydantic import validate_call
from pydantic_extra_types.color import Color
from PySide6.QtCore import Qt, SignalInstance
from PySide6.QtWidgets import QLabel, QSizePolicy, QWidget

from src.Model.Data.type import ImageArray
from src.Model.utils import read_image, unify_image_shape

from ..ui.ImageViewer_ui import Ui_ImageViewer


class ImageViewer(QWidget, Ui_ImageViewer):
    class ImageData(TypedDict):
        file_name: str
        original: ImageArray
        # modified: ImageArray | None

    images_data: list[ImageData] = []
    background: Literal["white", "black"] = "black"

    @property
    def current_image(self) -> ImageArray | None:
        return self.imageView.imageItem.image

    @property
    def current_original(self) -> ImageArray | None:
        if not self.images_data:
            return None
        if self.imageView.nframes() == 1:
            return self.images_data[0]["original"]
        else:
            return self.images_data[self.imageView.currentIndex]["original"]

    def __init__(self, parent) -> None:
        super().__init__(parent=parent)

        # 在setupUi()前完成对pyqt_graph的配置
        pyqtgraph.setConfigOption(
            "imageAxisOrder", "row-major"
        )  # 设置图像显示以行为主（横置）

        self.setupUi(self)

        self.imageView.ui.roiPlot.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed
        )

        self.label_image_name = QLabel(
            parent=self.imageView.ui.layoutWidget,
        )
        self.label_image_name.resize(500, 50)
        self.label_image_name.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.label_image_name.setStyleSheet("color: white")
        self.label_image_name.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.onImageChanged: SignalInstance = self.imageView.imageItem.sigImageChanged
        self.onFrameChanged: SignalInstance = self.imageView.sigTimeChanged
        self.onFrameChanged.connect(self.flush_showing_name)

    @validate_call
    def show_images(
        self,
        *image_files: ImageArray | Path,
        autoRange: bool = True,
        autoHistogramRange=True,
        autoLevels=True,
        levels=None,
    ) -> None:
        if not image_files:
            return
        self.images_data = []
        for f in image_files:
            if isinstance(f, Path):
                self.images_data.append(
                    {"file_name": f.name, "original": read_image(f)}
                )
            else:
                self.images_data.append({"file_name": "", "original": f})
        img = (
            self.images_data[0]["original"]
            if len(self.images_data) == 1
            else np.asarray(
                unify_image_shape(
                    [i["original"] for i in self.images_data], Color("red")
                )
            )
        )
        self.imageView.setImage(
            img,
            autoRange=autoRange,
            autoLevels=autoLevels,
            autoHistogramRange=autoHistogramRange,
            levels=levels,
        )
        self.change_view_background()
        self.flush_showing_name()

    def change_view_background(self, color: Literal["white", "black"] | None = None):
        if self.current_image is None:
            return
        if color == self.background:
            return
        if color is None:
            color = "white" if np.average(self.current_image) < 128 else "black"
        if color == "white":
            self.imageView.view.setBackgroundColor("white")
            self.label_image_name.setStyleSheet("color: black")
            self.background = "white"
        else:
            self.imageView.view.setBackgroundColor("black")
            self.label_image_name.setStyleSheet("color: white")
            self.background = "black"

    def set_current_image(self, image: ImageArray) -> None:
        self.imageView.imageItem.setImage(image)

    def block_SigImageChanged(self, state: bool) -> None:
        self.imageView.imageItem.blockSignals(state)

    def set_label_text(self, text: str) -> None:
        self.label_image_name.setText(text)
        # self.label_image_name.update()

    def get_label_text(self) -> str:
        return self.label_image_name.text()

    def flush_showing_name(self) -> None:
        self.set_label_text(self.images_data[self.imageView.currentIndex]["file_name"])

    def toggle_tools(self, state: bool) -> None:
        # 隐藏直方图，菜单按钮，ROI
        if state:
            self.imageView.ui.histogram.show()
            self.imageView.ui.menuBtn.show()
            self.imageView.ui.roiBtn.show()
        else:
            self.imageView.ui.histogram.hide()
            self.imageView.ui.menuBtn.hide()
            self.imageView.ui.roiBtn.hide()

    def clear(self) -> None:
        self.set_label_text("")
        self.imageView.clear()
