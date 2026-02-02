import time
from pathlib import Path

from loguru import logger as log
from PySide6.QtWidgets import QFileDialog

from src.Model.Data.const import ReclipMethod
from src.Model.Data.data import ReclipData, StyleData
from src.Model.Data.settings import (
    guiSettings,
    lineDetectorSettings,
    pathSettings,
    reclipSettings,
)
from src.Model.Data.type import FilePath, JsonPath
from src.Model.MainTask.Reclip import ReclipThread, style_restitched_clips
from src.Model.utils import get_sysfonts, read_image
from src.View import TabReclip_View
from src.ViewModel.binding.bind_data import bind_data


class TabReclip_VM(TabReclip_View):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainWindow = parent
        self.reclipThread: ReclipThread | None = None

        self.pathSettings = pathSettings
        self.reclipSettings = reclipSettings
        self.lineDetectorSettings = lineDetectorSettings
        self.styleData = StyleData()
        self.style_data_path: JsonPath | None = None

        bind_data(self.checkBox_live_preview, self.reclipSettings, "live_preview")
        bind_data(
            self.comboBox_clip_align, self.reclipSettings, "clip_align", use_index=True
        )
        bind_data(
            self.comboBox_reclip_method, self.reclipSettings, "method", use_index=True
        )
        bind_data(self.spinBox_clip_margin, self.reclipSettings, "clip_margin")
        bind_data(
            self.spinBox_each_line_bar_num, self.reclipSettings, "bar_num_each_line"
        )
        bind_data(
            self.spinBox_each_line_ength, self.reclipSettings, "bar_num_line_max_length"
        )
        bind_data(self.checkBox_clip_resize, self.reclipSettings, "clip_resize")
        bind_data(
            self.doubleSpinBox_resize_threshold,
            self.reclipSettings,
            "clip_resize_threshold",
        )

        bind_data(self.lineEdit_title, self.styleData, "title")
        bind_data(self.doubleSpinBox_margin_height, self.styleData, "margin_height")
        bind_data(self.doubleSpinBox_margin_width, self.styleData, "margin_width")
        bind_data(self.doubleSpinBox_margin_title, self.styleData, "margin_title")
        bind_data(self.comboBox_font_name, self.reclipSettings, "font_name")

        guiSettings.add_observer_handler(
            "imageViewer_show_tools", self.ImageViewer.toggle_tools
        )
        self.pathSettings.add_observer_handlers(
            ["main_out_dir", "score_title"], lambda v: self.handle_working_dir_changed()
        )
        self.reclipSettings.add_observer_handler(
            "method",
            lambda v: [
                self.spinBox_each_line_bar_num.setDisabled(
                    v == ReclipMethod.FILL_MAX_WIDTH
                ),
                self.spinBox_each_line_ength.setDisabled(
                    v == ReclipMethod.FIXED_BAR_NUM
                ),
            ],
        )

        self.pushButton_reclip.clicked.connect(self.start_reclip)
        self.pushButton_show_style.clicked.connect(self.show_style)
        self.pushButton_open_style.clicked.connect(self.handle_open_style)
        self.pushButton_save_style.clicked.connect(self.handle_save_style)

        self.sys_fonts = get_sysfonts()
        self.sys_font_names = list(self.sys_fonts.keys())
        self.check_font()
        self.update_font_name_combox()

    @property
    def font_path(self) -> FilePath:
        assert self.sys_fonts
        return self.sys_fonts[self.reclipSettings.font_name]

    def check_font(self) -> None:
        font_name = self.reclipSettings.font_name
        if font_name == "" or font_name not in self.sys_font_names:
            self.reclipSettings.font_name = self.sys_font_names[0]

    def update_font_name_combox(self) -> None:
        self.comboBox_font_name.blockSignals(True)
        self.comboBox_font_name.clear()
        self.comboBox_font_name.addItems(self.sys_font_names)
        self.comboBox_font_name.setCurrentText(self.reclipSettings.font_name)
        self.comboBox_font_name.blockSignals(False)

    def flush_preview(self) -> None:
        working_dir = self.pathSettings.working_dir
        path = list(working_dir.glob(f"{working_dir.name}*[0-9]*"))
        if not path:
            log.info(f"没有在{working_dir}下发现{working_dir.name}*[0-9]*文件")
            return
        self.ImageViewer.show_images(*path)

    def start_reclip(self) -> None:
        if self.reclipThread:
            log.warning("当前重分割任务仍未结束，请稍后重试")
            return
        if not self.pathSettings.working_dir.exists():
            log.warning(f"当前工作目录{self.pathSettings.working_dir}不存在")
            return

        self.reclipThread = ReclipThread(
            self.reclipSettings,
            self.lineDetectorSettings,
            self.pathSettings.working_dir,
            self.font_path,
            self.styleData,
        )
        self.reclipThread.finished.connect(self.flush_preview)
        self.reclipThread.destroyed.connect(lambda: setattr(self, "reclipThread", None))
        self.reclipThread.start()

    def show_style(self) -> None:
        working_dir = self.pathSettings.working_dir
        filename = working_dir.name + "-reclip" + reclipSettings.saving_format
        if not (working_dir / filename).exists():
            log.warning(f"Recliped image not found:{working_dir / filename}")
            return
        restitched_image = read_image(working_dir / filename)
        if not (working_dir / "ReclipData.json").exists():
            log.warning(f"ReclipData not found:{working_dir / 'ReclipData.json'}")
            return
        reclip_data = ReclipData.load_from_file(working_dir / "ReclipData.json")

        style_restitched_clips(
            log,
            working_dir,
            self.reclipSettings,
            restitched_image,
            self.styleData,
            font_path=self.font_path,
            reclip_data=reclip_data,
        )
        self.flush_preview()

    def load_style(self, path: JsonPath) -> None:
        self.style_data_path = path
        style = StyleData.load_from_file(path)
        for prop in StyleData.model_fields.keys():
            setattr(self.styleData, prop, getattr(style, prop))
        log.debug(f"StyleData Loaded: {path}")

    def handle_working_dir_changed(self) -> None:
        working_dir = self.pathSettings.working_dir
        if self.style_data_path == (working_dir / "StyleData.json"):
            return
        if self.style_data_path:
            self.styleData.save_to_file(self.style_data_path)
            self.style_data_path = None
        if (path := (working_dir / "StyleData.json")).exists():
            self.load_style(path)
        else:
            self.styleData.title = working_dir.name
            self.ImageViewer.clear()

    def handle_open_style(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            dir=self.pathSettings.working_dir.as_posix(),
            filter="StyleData (StyleData*.json)",
        )
        if path == "":
            return
        self.load_style(Path(path))
        self.show_style()

    def handle_save_style(self) -> None:
        name = f"StyleData_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json"
        path, _ = QFileDialog.getSaveFileName(
            dir=(self.pathSettings.working_dir / name).as_posix(),
            filter="StyleData (*.json)",
        )
        if path == "":
            return
        self.styleData.save_to_file(Path(path))
        log.success(f"StyleData saved as {path}")

    def closeEvent(self, event):
        if self.style_data_path:
            self.styleData.save_to_file(self.style_data_path)
        elif self.styleData != StyleData() and self.pathSettings.working_dir.exists():
            self.styleData.save_to_file(
                self.pathSettings.working_dir / "StyleData.json"
            )
        super().closeEvent(event)
