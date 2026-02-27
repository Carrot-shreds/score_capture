import asyncio
from pathlib import Path
from typing import cast

import cv2
import numpy as np
from loguru import logger as log
from pyqtgraph import ImageItem
from PySide6.QtCore import QLineF, QPoint, QPointF, QRectF, Qt
from PySide6.QtWidgets import QFileDialog

from src.Model.Data.settings import (
    captureSettings,
    guiSettings,
    pathSettings,
    videoCropSettings,
)
from src.Model.Data.type import ImageArray
from src.Model.utils import read_image
from src.View.TabCrop import CropViewBox, TabCrop_View
from src.ViewModel.binding.bind_data import bind_data


class TabCrop_VM(TabCrop_View):
    def __init__(self, parent):
        super().__init__(parent)
        self.mainWindow = parent

        self.pathSettings = pathSettings
        self.guiSettings = guiSettings
        self.captureSettings = captureSettings
        self.videoCropSettings = videoCropSettings

        self.video_path: Path | None = None
        self.preview_frame: ImageArray | None = None
        self.overlay: ImageArray | None = None
        self.crop_region = self.videoCropSettings.crop_region
        self.line_thickness = 4  # Must be an even number
        self.drag_anchor_radius = 10
        # [0,1,2,3] -> TopLeft,TopRight,BottomLeft,BottomRight Archor
        # [-1] -> Draging the line (the rect border)
        self.dragging_anchor_num: int | None = None
        self.dragging_last_point: QPointF | None = None

        self.viewBox = cast(CropViewBox, self.ImageViewer.imageView.view)
        self.viewBox.dragStarted.connect(self.handle_draging_start)
        self.viewBox.dragMoved.connect(self.handle_draging_move)
        self.viewBox.dragFinished.connect(self.handle_draging_finish)
        self.viewBox.regionSelected.connect(self.handle_region_select)
        self.viewBox.hoverMoved.connect(self.handle_hover_moved)
        self.overlay_item = ImageItem()
        self.last_overlay_region = None
        self.viewBox.addItem(self.overlay_item)

        bind_data(self.spinBox_x, self.crop_region, "x")
        bind_data(self.spinBox_y, self.crop_region, "y")
        bind_data(self.spinBox_width, self.crop_region, "width")
        bind_data(self.spinBox_height, self.crop_region, "height")
        bind_data(
            self.doubleSpinBox_start_time,
            self.videoCropSettings,
            "start_time",
            when_finished=True,
        )
        bind_data(
            self.checkBox_skip_nonkey_frames,
            self.videoCropSettings,
            "skip_nonkey_frames",
        )
        bind_data(self.doubleSpinBox_interval, self.captureSettings, "interval_time")
        bind_data(self.checkBox_invert_image, self.captureSettings, "if_invert_image")

        guiSettings.add_observer_handler(
            "imageViewer_show_tools", self.ImageViewer.toggle_tools
        )

        self.crop_region.add_observer_handlers(
            ["x", "y", "width", "height"], lambda v: self.flush_overlay(), False
        )
        self.videoCropSettings.add_observer_handler(
            "start_time",
            lambda v: [
                asyncio.ensure_future(self.extract_preview_frame()),
                self.flush_preview(),
            ],
            False,
        )

        self.pushButton_open_video.pressed.connect(
            lambda: asyncio.ensure_future(self.handle_open_video())
        )
        self.pushButton_start_cropping.pressed.connect(
            lambda: asyncio.ensure_future(self.start_cropping())
        )

    @property
    def preview_frame_path(self) -> Path:
        return self.pathSettings.main_out_dir / "preview_frame.jpg"

    @property
    def drag_anchors_pos(self) -> list[tuple[int, int]]:
        region = self.crop_region
        x0, y0 = region.x, region.y
        x1, y1 = region.x + region.width, region.y + region.height
        # Keep the rect around the crop reigon
        offset = int(self.line_thickness / 2)
        x0 -= offset + 1  # Test result
        y0 -= offset + 1
        x1 += offset
        y1 += offset
        # TopLeft, TopRight, BottomLeft, BottomRight
        return [(x0, y0), (x1, y0), (x0, y1), (x1, y1)]

    @property
    def drag_anchor_points(self) -> list[QPoint]:
        return [QPoint(*p) for p in self.drag_anchors_pos]

    def update_region_from_border_dragging(self, point: QPointF):
        if self.dragging_last_point is None:
            return
        diff = point - self.dragging_last_point
        try:
            # Validate x and y together after setting
            old_region = self.crop_region.region
            with self.crop_region.no_notify():
                with self.crop_region.delay_validate():
                    self.crop_region.x += int(diff.x())
                    self.crop_region.y += int(diff.y())
            self.flush_overlay()
        except ValueError:
            self.crop_region.region = old_region
        else:
            self.dragging_last_point = point

    def update_region_from_anchor(
        self, point: QPointF | QPoint, anchor_num: int
    ) -> None:
        point = point.toPoint() if isinstance(point, QPointF) else point
        tl, tr, bl, br = [QPoint(*p) for p in self.drag_anchors_pos]
        match anchor_num:
            case 0:
                tl = point
            case 1:
                tr = point
            case 2:
                bl = point
            case 3:
                br = point
        offset = int(self.line_thickness / 2)
        if anchor_num in [0, 3]:  # TopLeft or BottomRight
            x, y = tl.x(), tl.y()
            w, h = br.x() - tl.x(), br.y() - tl.y()
        else:  # TopRight or BottomLeft
            x, y = bl.x(), tr.y()
            w, h = tr.x() - bl.x(), bl.y() - tr.y()
        region = (  # Map border to inner region
            x + offset + 1,
            y + offset + 1,
            w - self.line_thickness - 1,
            h - self.line_thickness - 1,
        )
        try:
            old_region = self.crop_region.region
            with self.crop_region.no_notify():
                self.crop_region.region = region
            self.flush_overlay()
        except ValueError:
            self.crop_region.region = old_region

    def dragging_the_border(self, pos: QPointF) -> bool:
        # on the line (the border)
        anchors = self.drag_anchor_points
        lines = [
            QLineF(anchors[i[0]], anchors[i[1]])
            for i in [(0, 1), (0, 2), (1, 3), (2, 3)]
        ]
        for line in lines:
            if line.angle() == 0:  # Horizontal
                offset_point = QPointF(
                    self.drag_anchor_radius * 2, -self.line_thickness * 2
                )
            if line.angle() == 270:  # Vertical
                offset_point = QPointF(
                    -self.line_thickness * 2, self.drag_anchor_radius * 2
                )
            rect = QRectF(
                line.p1() + offset_point,
                line.p2() - offset_point,
            )
            if rect.contains(pos):
                return True
        return False

    def dragging_the_anchor(self, pos: QPointF) -> tuple[bool, int | None]:
        anchors = self.drag_anchor_points
        # on the anchor
        for i, anchor in enumerate(anchors):
            # The position was after the first movement.
            # So it would be far from the anchor if the mouse move fast.
            if QLineF(pos, anchor).length() <= self.drag_anchor_radius * 2:
                return True, i
        return False, None

    def handle_hover_moved(self, pos: QPointF) -> None:
        if self.ImageViewer.imageView.image is None:
            return

        dragging_anchor, num = self.dragging_the_anchor(pos)
        if dragging_anchor:
            if num in [0, 3]:
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            else:
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif self.dragging_the_border(pos):
            self.setCursor(Qt.CursorShape.OpenHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def handle_region_select(self, rectf: QRectF) -> None:
        rect = rectf.toRect()
        try:
            self.crop_region.region = rect.x(), rect.y(), rect.width(), rect.height()
        except ValueError:
            pass

    def handle_draging_start(self, pos: QPointF) -> None:
        self.viewBox.dragging_anchor, self.dragging_anchor_num = (
            self.dragging_the_anchor(pos)
        )
        if self.dragging_anchor_num is None and self.dragging_the_border(pos):
            self.viewBox.dragging_anchor = True
            self.dragging_anchor_num = -1
            self.dragging_last_point = pos
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def handle_draging_move(self, pos: QPointF) -> None:
        if self.dragging_anchor_num is None:
            return
        if self.dragging_anchor_num >= 0:
            self.update_region_from_anchor(pos, self.dragging_anchor_num)
        elif self.dragging_anchor_num == -1:
            self.update_region_from_border_dragging(pos)

    def handle_draging_finish(self, pos: QPointF) -> None:
        if self.dragging_anchor_num is None:
            return
        self.viewBox.dragging_anchor = False
        self.dragging_anchor_num = None
        self.dragging_last_point = None

    async def load_ffmpge(self) -> None:
        if hasattr(self, "ffmpeg") and self.ffmpeg:
            return

        from pyffmpeg import FFmpeg, Paths

        ff_path = Paths()
        ff_exec_path = Path(ff_path.bin_path) / ("ffmpeg" + ff_path._ffmpeg_ext)
        if not ff_exec_path.exists():
            log.info(self.tr("Extracting FFmpeg to {}").format(ff_exec_path))
            self.ffmpeg = await asyncio.to_thread(FFmpeg)
        else:
            self.ffmpeg = FFmpeg()
        self.ff_exec_path = ff_exec_path

    async def handle_open_video(self) -> None:
        dir = (
            self.pathSettings.working_dir
            if not self.videoCropSettings.videos_dir
            else self.videoCropSettings.videos_dir
        )
        path, _ = QFileDialog.getOpenFileName(
            dir=dir.as_posix(),
            filter="Video (*.mp4 *.avi *.mov *.mkv)",
        )
        if path == "":
            return
        await self.load_ffmpge()
        self.video_path = Path(path).resolve()
        self.videoCropSettings.videos_dir = self.video_path.parent
        self.pathSettings.score_title = self.video_path.with_suffix("").name
        log.info(self.tr("Using video path: {}").format(self.video_path))
        await self.extract_preview_frame()
        self.flush_overlay()
        self.flush_preview(autoRange=True)

    async def extract_preview_frame(self) -> None:
        if not self.video_path:
            return
        options = [
            f"-ss {self.videoCropSettings.start_time}",  # skip to start time
            f'-i "{self.video_path.as_posix()}"',  # input video path
            "-frames:v 1",  # take one frame
            " -q:v 5",  # jpeg quality
            f'"{self.preview_frame_path.as_posix()}"',  # saving path
        ]
        if self.videoCropSettings.skip_nonkey_frames:
            options.insert(0, "-skip_frame nokey")  # Only keep key frames
        if not (p := self.preview_frame_path.parent).exists():
            p.mkdir()
        await asyncio.to_thread(self.ffmpeg.options, " ".join(options))
        self.preview_frame = read_image(self.preview_frame_path)
        self.crop_region.image_shape = self.preview_frame.shape[0:2]
        try:
            self.crop_region.model_validate(self.crop_region)
        except ValueError:
            self.crop_region.region = (0, 0, 100, 100)

    async def start_cropping(self) -> None:
        if not self.video_path:
            log.warning(self.tr("Video Path is None. Please open a video first."))
            return
        if not self.mainWindow.check_working_dir():
            return
        self.pushButton_start_cropping.setEnabled(False)

        capture_fps = 1 / self.captureSettings.interval_time

        x, y, w, h = self.crop_region.region
        options = [
            f"-ss {self.videoCropSettings.start_time}",  # skip to start time
            f'-i "{self.video_path.as_posix()}"',  # input video path
            "-vf",
            f'"fps={capture_fps},' + f'crop={w}:{h}:{x}:{y}"',
            " -q:v 5",  # jpeg quality
            f'"{(self.pathSettings.working_dir / f"capture%d{self.captureSettings.save_format}").as_posix()}"',  # saving path
        ]
        if self.videoCropSettings.skip_nonkey_frames:
            options.insert(0, "-skip_frame nokey")  # Only keep key frames

        log.info(
            self.tr("Running FFmepg command: {}").format(
                " ".join([self.ff_exec_path.as_posix()] + options)
            )
        )
        await asyncio.to_thread(self.ffmpeg.options, " ".join(options))
        capture_count = len(list(self.pathSettings.working_dir.glob("capture*")))
        log.success(
            self.tr("Cropping finished, {} captures saved").format(capture_count)
        )
        self.pushButton_start_cropping.setEnabled(True)

    def flush_overlay(self) -> None:
        if self.preview_frame is None:
            return
        if self.crop_region.region == self.last_overlay_region:
            return

        self.overlay = np.zeros(  # With alpha channel
            (self.preview_frame.shape[0], self.preview_frame.shape[1], 4)
        )
        anchors_pos = self.drag_anchors_pos
        color = (0, 255, 0, 255)  # Green @BGRA
        cv2.rectangle(
            self.overlay, anchors_pos[0], anchors_pos[3], color, self.line_thickness
        )
        for p in anchors_pos:
            cv2.circle(self.overlay, p, self.drag_anchor_radius, color, -1)

        self.overlay_item.setImage(self.overlay, autoLevels=False, levels=[0, 255])
        self.last_overlay_region = self.crop_region.region

    def flush_preview(self, autoRange: bool = False) -> None:
        if self.preview_frame is None:
            return
        self.ImageViewer.show_images(self.preview_frame, autoRange=autoRange)
