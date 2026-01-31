from typing import cast

import mss
import mss.factory
import numpy as np
from loguru import logger as log
from pydantic import ValidationError
from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QMoveEvent, QResizeEvent

from src.Model.Data.settings import captureSettings, locateSettings
from src.Model.utils import qrect2array, set_window_always_on_top
from src.View import DialogLocate_View
from src.ViewModel.binding.bind_data import bind_data


class DialogLocate_VM(DialogLocate_View):
    def __init__(self, parent=None):
        super().__init__()
        self.scaling = self.screen().devicePixelRatio()  # 获取缩放比例

        self.locateSettings = locateSettings
        self.captureSettings = captureSettings

        bind_data(self.spinBox_region_x, self.locateSettings.region_data, "x")
        bind_data(self.spinBox_region_y, self.locateSettings.region_data, "y")
        bind_data(self.spinBox_region_width, self.locateSettings.region_data, "width")
        bind_data(self.spinBox_region_height, self.locateSettings.region_data, "height")
        bind_data(self.checkBox_live_locate, self.locateSettings, "live_locate")
        bind_data(
            self.checkBox_dialog_always_on_top,
            self.locateSettings,
            "window_always_on_top",
        )
        bind_data(self.checkBox_reverse_image, self.captureSettings, "if_reverse_image")

        self.locateSettings.region_data.add_observer_handlers(
            ["x", "y", "width", "height"],
            lambda v: self.setGeometry(*self.locateSettings.region_data.region)
            if not self.m_drag_edge or self.m_drag_edge == (0, 0, 0, 0)
            else None,
        )
        self.locateSettings.add_observer_handler(
            "window_opacity", lambda v: self.setWindowOpacity(v)
        )
        self.locateSettings.add_observer_handler(
            "window_always_on_top",
            lambda v: set_window_always_on_top(self, v) if not self.mini_mode else None,
        )

        self.OutMiniMode.connect(
            lambda: [
                set_window_always_on_top(
                    self, self.locateSettings.window_always_on_top
                ),
                self.setWindowOpacity(self.locateSettings.window_opacity),
            ]
        )
        self.pushButton_locate.clicked.connect(self.locate)
        self.pushButton_minimize.clicked.connect(self.showMinimized)
        self.pushButton_close.clicked.connect(self.close)

    def locate(self) -> None:
        """
        定位范围，并更新显示
        """
        # TODO 多屏幕屏幕选择
        # 使用frameGeometry以包含标题栏尺寸
        region = cast(
            tuple[int, int, int, int],
            tuple(
                int(i)
                for i in np.ceil(qrect2array(self.frameGeometry()) * self.scaling)
            ),
        )
        if region == self.locateSettings.region_data.region:
            return
        try:
            self.locateSettings.region_data.region = region
        except ValidationError as e:
            log.warning(f"Invalid region:{region}")
            log.debug(e)
            return
        if not self.locateSettings.live_locate:
            log.success(f"update region: {tuple(int(r) for r in region)}")
        if self.locateSettings.window_auto_close:
            self.close()

    def show(self) -> None:
        self.setGeometry(*self.locateSettings.region_data.region)
        super().show()  # 在show之后才能获取到准确geometry
        self.showNormal()  # 从最小化恢复窗口显示
        self.raise_()  # 在最前端显示
        self.activateWindow()  # 切换窗口焦点

        # 计算更新offset
        self.scaling = self.screen().devicePixelRatio()  # 获取缩放比例
        self.locateSettings.locate_offset = tuple(
            qrect2array(self.geometry()) - qrect2array(self.frameGeometry())
        )
        self.setGeometry(*self.locateSettings.region_data.region)
        log.debug(f"Scrren scaling: {self.scaling}")
        log.debug(f"Locate offset: {self.locateSettings.locate_offset}")

    def close(self, /) -> bool:
        self.setVisible(False)
        return True

    def moveEvent(self, event: QMoveEvent, /) -> None:
        if self.locateSettings.live_locate:
            try:
                self.locate()
            except ValidationError:
                return
        super().moveEvent(event)

    def resizeEvent(self, event: QResizeEvent, /) -> None:
        if self.locateSettings.live_locate:
            try:
                self.locate()
            except ValidationError:
                return
        super().resizeEvent(event)

    def move(self, x: QPoint | int, y: int = 0):
        if isinstance(x, int):
            point = QPoint(x, y)
        else:
            point = x

        if self.locateSettings.window_limit_move:
            with mss.mss() as sct:
                monitor = sct.monitors[self.locateSettings.region_data.monitor_num]
                if (
                    point.x() < 0
                    or point.y() < 0
                    or point.x() + self.width() > monitor["width"]
                    or point.y() + self.height() > monitor["height"]
                ):
                    return
        super().move(point)

    def setGeometry(
        self, a0: QRect | int, a1: int = 0, a2: int = 0, a3: int = 0
    ) -> None:
        # 将两种参数形式都转换为 QRect
        if isinstance(a0, QRect):
            rect = a0
        else:
            rect = QRect(a0, a1, a2, a3)

        if rect == self.frameGeometry():
            return
        if self.locateSettings.window_limit_move:
            with mss.mss() as sct:
                monitor = sct.monitors[self.locateSettings.region_data.monitor_num]
                if (
                    rect.x() < 0
                    or rect.y() < 0
                    or rect.x() + rect.width() > monitor["width"]
                    or rect.y() + rect.height() > monitor["height"]
                ):
                    return

        super().setGeometry(
            *(
                qrect2array(rect) / self.scaling
                + np.asarray(self.locateSettings.locate_offset)
            ).astype(int)
        )
