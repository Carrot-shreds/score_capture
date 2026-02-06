from copy import deepcopy
from pathlib import Path

import cv2
from loguru import logger as log
from PySide6.QtWidgets import QFileDialog

from src.Model.Data.const import PreviewLines
from src.Model.Data.settings import (
    captureSettings,
    guiSettings,
    lineDetectorSettings,
    locateSettings,
    pathSettings,
    previewSettings,
)
from src.Model.Data.type import ImagePath, Line
from src.Model.image_process import (
    detect_horizontal_lines,
    detect_vertical_lines,
    image_pre_process,
    reverse_image,
)
from src.Model.utils import order_path, read_image, save_image, screenshot
from src.View import TabPreview_View
from src.ViewModel.binding.bind_data import bind_data


class TabPreview_VM(TabPreview_View):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainWindow = parent

        self.pathSettings = pathSettings
        self.locateSettings = locateSettings
        self.regionData = self.locateSettings.region_data
        self.captureSettings = captureSettings
        self.detectorSettings = lineDetectorSettings
        self.previewSetting = previewSettings

        bind_data(
            self.doubleSpinBox_detect_coefficient_horizontal,
            self.detectorSettings,
            "coefficient_horizontal",
        )
        bind_data(
            self.doubleSpinBox_detect_coefficient_vertical,
            self.detectorSettings,
            "coefficient_vertical",
        )
        bind_data(
            self.spinBox_h_reverse_thickness_threshold,
            self.detectorSettings,
            "h_reverse_thickness_threshold",
        )
        bind_data(
            self.doubleSpinBox_h_reverse_pixel_threshold,
            self.detectorSettings,
            "h_reverse_pixel_threshold",
        )
        bind_data(
            self.checkBox_reverse_horizontal,
            self.previewSetting,
            "show_reversed_horizontal",
        )
        bind_data(
            self.comboBox_line_type,
            self.previewSetting,
            "preview_lines",
            use_index=True,
        )
        bind_data(self.checkBox_save_preview, self.previewSetting, "save_preview")
        bind_data(self.checkBox_live_preview, self.previewSetting, "live_preview")
        bind_data(self.checkBox_live_detect, self.previewSetting, "live_detect")

        guiSettings.add_observer_handler(
            "imageViewer_show_tools", self.ImageViewer.toggle_tools
        )
        self.previewSetting.add_observer_handlers(
            ["preview_lines", "show_reversed_horizontal"],
            lambda v: self.preview_lines() if self.previewSetting.live_detect else None,
        )
        self.previewSetting.add_observer_handler(
            "live_preview", self.toggle_live_preview
        )
        self.previewSetting.add_observer_handler("live_detect", self.toggle_live_detect)

        self.lambda_preview_region = lambda v: self.preview_region()
        self.lambda_preview_lines = lambda v: self.preview_lines()
        self.pushButton_update_image.clicked.connect(self.preview_region)
        self.pushButton_open_image.clicked.connect(self.select_image)
        self.pushButton_reverse_image.clicked.connect(self.reverse_image)
        self.pushButton_detect_lines.clicked.connect(self.preview_lines)
        self.pushButton_clear_lines.clicked.connect(self.clear_lines)
        self.pushButton_glob_image.clicked.connect(self.glob_image)

    def preview_lines(self) -> None:
        if self.ImageViewer.current_image is None:
            return
        original_image = self.ImageViewer.current_original
        if original_image is None:
            return
        gray_image = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY)

        lines: list[Line] = []
        image_draw = deepcopy(original_image)
        match self.previewSetting.preview_lines:
            case PreviewLines.ONLY_H:
                lines += detect_horizontal_lines(
                    gray_image,
                    self.detectorSettings.coefficient_horizontal,
                    self.previewSetting.show_reversed_horizontal,
                    self.detectorSettings.h_reverse_pixel_threshold,
                    self.detectorSettings.h_reverse_thickness_threshold,
                )
            case PreviewLines.ONLY_V:
                if not self.previewSetting.show_reversed_horizontal:
                    lines += detect_vertical_lines(
                        gray_image,
                        coefficient=self.detectorSettings.coefficient_vertical,
                    )
            case PreviewLines.ALL:
                h_lines = detect_horizontal_lines(
                    gray_image,
                    self.detectorSettings.coefficient_horizontal,
                    self.previewSetting.show_reversed_horizontal,
                    self.detectorSettings.h_reverse_pixel_threshold,
                    self.detectorSettings.h_reverse_thickness_threshold,
                )
                if not self.previewSetting.show_reversed_horizontal:
                    lines += detect_vertical_lines(
                        gray_image, h_lines, self.detectorSettings.coefficient_vertical
                    )
                lines += h_lines
        for line in lines:
            line.draw(image_draw)

        if self.previewSetting.live_detect:
            self.ImageViewer.block_SigImageChanged(True)  # block onImageChanged Signal
        self.ImageViewer.set_current_image(image_draw)
        self.ImageViewer.block_SigImageChanged(False)
        label_text = self.ImageViewer.get_label_text().replace(" (reversed)", "")
        label_text += " (detected)" if label_text.find("(detected)") >= 0 else ""
        self.ImageViewer.set_label_text(label_text)
        if self.previewSetting.save_preview:
            save_image(
                self.pathSettings.main_out_dir / "preview_linesDetected.png", image_draw
            )

    def clear_lines(self) -> None:
        original = self.ImageViewer.current_original
        if original is None:
            return
        self.ImageViewer.set_current_image(original)
        self.ImageViewer.set_label_text(
            self.ImageViewer.get_label_text().replace(" (detected)", "")
        )

    def toggle_live_preview(self, state: bool) -> None:
        """切换启用实时预览"""
        if state:
            self.regionData.add_observer_handler("region", self.lambda_preview_region)
            self.preview_region()
        else:
            try:
                self.regionData.remove_observer_handler(
                    "region", self.lambda_preview_region
                )
            except ValueError:
                return

    def toggle_live_detect(self, state: bool) -> None:
        """切换启用实时检测"""
        if state:
            self.detectorSettings.add_observer_handlers(
                [
                    "coefficient_horizontal",
                    "coefficient_vertical",
                    "h_reverse_thickness_threshold",
                    "h_reverse_pixel_threshold",
                ],
                self.lambda_preview_lines,
            )
            self.ImageViewer.onImageChanged.connect(self.preview_lines)
            self.preview_lines()
        else:
            try:
                self.detectorSettings.remove_observer_handlers(
                    [
                        "coefficient_horizontal",
                        "coefficient_vertical",
                        "h_reverse_thickness_threshold",
                        "h_reverse_pixel_threshold",
                    ],
                    self.lambda_preview_lines,
                )
            except ValueError:
                return
            self.ImageViewer.onImageChanged.disconnect(self.preview_lines)

    def preview_region(self) -> None:
        """显示region区域的预览"""
        if not self.locateSettings.live_locate:
            log.debug(f"preview region: {self.regionData.region}")
        img = image_pre_process(
            screenshot(
                region_data=self.regionData, capture_tool=self.captureSettings.tool
            ),
            self.captureSettings.if_reverse_image,
        )
        if self.previewSetting.save_preview:
            save_image(self.pathSettings.main_out_dir / "preview.png", img)
        self.ImageViewer.show_images(img)
        self.ImageViewer.set_label_text(f"Preview region: {self.regionData.region}")

    def open_image(self, image_path: ImagePath) -> None:
        self.ImageViewer.show_images(read_image(image_path))

    def select_image(self) -> None:
        path, _ = QFileDialog.getOpenFileNames(
            dir=self.pathSettings.working_dir.as_posix(), filter="Images (*.png *.jpg)"
        )
        if path == "":
            return
        self.ImageViewer.show_images(*map(Path, path))

    def reverse_image(self) -> None:
        if self.ImageViewer.current_image is not None:
            self.ImageViewer.set_current_image(
                reverse_image(self.ImageViewer.current_image)
            )
        reversed_str = " (reversed)"
        if (current_text := self.ImageViewer.get_label_text()).find(reversed_str) >= 0:
            self.ImageViewer.set_label_text(current_text.replace(reversed_str, ""))
        else:
            self.ImageViewer.set_label_text(current_text + reversed_str)

    def glob_image(self) -> None:
        def _ok():
            self.ImageViewer.show_images(
                *order_path(
                    list(
                        Path(dialog.lineEdit_path.text()).glob(
                            dialog.comboBox_glob.currentText()
                        )
                    )
                )
            )
            dialog.close()

        dialog = self.create_glob_dialog()
        dialog.comboBox_glob.addItem(f"{self.pathSettings.working_dir.name}*[0-9].*")
        dialog.lineEdit_path.setText(self.pathSettings.working_dir.as_posix())
        dialog.pushButton_select_path.clicked.connect(
            lambda: (
                dialog.lineEdit_path.setText(t)
                if (t := QFileDialog.getExistingDirectory()) != ""
                else None
            )
        )
        dialog.pushButton_ok.clicked.connect(_ok)
        dialog.show()
