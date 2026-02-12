from typing import NamedTuple, TypedDict

from PySide6.QtCore import QPoint, QRect, QSize, Qt, QTimer, Signal
from PySide6.QtGui import QKeySequence, QMouseEvent
from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QWidget

from src.Model.utils import set_window_always_on_top

from .ui.DialogLocate_ui import Ui_DialogLocate


class EdgeTuple(NamedTuple):
    Left: bool
    Right: bool
    Top: bool
    Bottom: bool


class Edges(TypedDict):
    Left: EdgeTuple
    Right: EdgeTuple
    Top: EdgeTuple
    Bottom: EdgeTuple
    TopLeft: EdgeTuple
    TopRight: EdgeTuple
    BottomLeft: EdgeTuple
    BottomRight: EdgeTuple


_Edge: Edges = {
    "Left": EdgeTuple(Left=True, Right=False, Top=False, Bottom=False),
    "Right": EdgeTuple(Left=False, Right=True, Top=False, Bottom=False),
    "Top": EdgeTuple(Left=False, Right=False, Top=True, Bottom=False),
    "Bottom": EdgeTuple(Left=False, Right=False, Top=False, Bottom=True),
    "TopLeft": EdgeTuple(Left=True, Right=False, Top=True, Bottom=False),
    "TopRight": EdgeTuple(Left=False, Right=True, Top=True, Bottom=False),
    "BottomLeft": EdgeTuple(Left=True, Right=False, Top=False, Bottom=True),
    "BottomRight": EdgeTuple(Left=False, Right=True, Top=False, Bottom=True),
}

_CursorShape = {
    _Edge["Top"]: Qt.CursorShape.SizeVerCursor,
    _Edge["Bottom"]: Qt.CursorShape.SizeVerCursor,
    _Edge["Left"]: Qt.CursorShape.SizeHorCursor,
    _Edge["Right"]: Qt.CursorShape.SizeHorCursor,
    _Edge["TopLeft"]: Qt.CursorShape.SizeFDiagCursor,
    _Edge["BottomRight"]: Qt.CursorShape.SizeFDiagCursor,
    _Edge["TopRight"]: Qt.CursorShape.SizeBDiagCursor,
    _Edge["BottomLeft"]: Qt.CursorShape.SizeBDiagCursor,
}


class DialogLocate_View(QDialog, Ui_DialogLocate):
    OutMiniMode = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # 去掉默认边框

        self.scaling = self.screen().devicePixelRatio()  # 获取缩放比例
        self.screen_size = self.screen().size()  # Virtual Size

        # shortcut
        self.pushButton_locate.setShortcut(QKeySequence("l"))
        self.pushButton_preview.setShortcut(QKeySequence("p"))
        self.checkBox_dialog_always_on_top.setShortcut(QKeySequence("F12"))

        # 自定义边框鼠标事件
        self.m_drag_start_pos: QPoint | None = None
        self.m_original_geometry: QRect | None = None
        self.m_drag_edge: EdgeTuple | None = None
        self.m_resize_margin: int = 8  # 边缘检测范围
        self.setMouseTracking(True)

        self.pushButton_toggle_show_mode = QPushButton(self)
        self.pushButton_toggle_show_mode.setMouseTracking(True)
        self.pushButton_toggle_show_mode.setGeometry(15, 15, 30, 30)
        self.pushButton_toggle_show_mode.setText("—")
        self.pushButton_toggle_show_mode.clicked.connect(self.toggle_mini_mode)
        self.pushButton_toggle_show_mode.setToolTip(self.tr("Toggle mini mode."))
        self.pushButton_toggle_capture = QPushButton(self)
        self.pushButton_toggle_capture.setMouseTracking(True)
        self.pushButton_toggle_capture.setGeometry(45, 15, 30, 30)
        self.pushButton_toggle_capture.setText("📷")
        self.pushButton_toggle_capture.setToolTip(self.tr("Toggle capture state"))
        self.lineEdit_score_title = QLineEdit(self)
        self.lineEdit_score_title.setGeometry(5, 35, 80, 20)
        self.lineEdit_score_title.setVisible(False)
        self.lineEdit_score_title.setToolTip(self.tr("Folder title"))

        self.widget.setStyleSheet("background:lightgray")
        self.widget.setMouseTracking(True)
        self.frame.setStyleSheet("background:white")
        self.frame.setMouseTracking(True)

        self.mini_mode: bool = False
        self.minimun_size_before_mini_mode: QSize = self.minimumSize()
        self.size_before_mini_mode: QSize = self.size()

    def toggle_mini_mode(self) -> None:
        self.mini_mode = not self.mini_mode
        for widget in self.frame.children():
            if isinstance(widget, QWidget):
                widget.setVisible(not self.mini_mode)
        if self.mini_mode:
            self.size_before_mini_mode = self.size()
            self.minimun_size_before_mini_mode = self.minimumSize()
            self.pushButton_toggle_show_mode.setGeometry(8, 4, 30, 30)
            self.pushButton_toggle_capture.setGeometry(50, 4, 30, 30)
            self.lineEdit_score_title.setVisible(True)
            self.setWindowOpacity(0.8)
            self.setMinimumSize(90, 60)
            self.resize(90, 60)
            set_window_always_on_top(self, True)
        else:
            self.setMinimumSize(self.minimun_size_before_mini_mode)
            self.resize(self.size_before_mini_mode)
            self.pushButton_toggle_show_mode.setGeometry(15, 15, 30, 30)
            self.pushButton_toggle_capture.setGeometry(45, 15, 30, 30)
            self.lineEdit_score_title.setVisible(False)
            self.OutMiniMode.emit()

    def flash_capture_button(self, msec: int, color: str) -> None:
        self.pushButton_toggle_capture.setStyleSheet(f"background-color:{color}")
        QTimer.singleShot(
            msec,
            lambda: self.pushButton_toggle_capture.setStyleSheet(
                "background-color:white"
            ),
        )

    def get_edge_at_position(self, pos) -> EdgeTuple:
        """检测鼠标位置所在的边缘"""
        rect = self.rect()
        x, y = pos.x(), pos.y()
        return EdgeTuple(
            x < self.m_resize_margin,
            x > rect.width() - self.m_resize_margin,
            y < self.m_resize_margin,
            y > rect.height() - self.m_resize_margin,
        )

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.m_drag_start_pos = event.globalPos()
            self.m_original_geometry = self.geometry()
            self.m_drag_edge = self.get_edge_at_position(event.pos())
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle_mini_mode()
        if event.button() == Qt.MouseButton.RightButton:
            self.showMinimized()

    def mouseMoveEvent(self, event: QMouseEvent):
        self.update_cursor_shape(event.pos())
        if not self.m_drag_start_pos or not self.m_original_geometry:
            return

        delta = event.globalPos() - self.m_drag_start_pos

        if self.m_drag_edge and any(self.m_drag_edge) and not self.mini_mode:
            x = (
                self.m_original_geometry.x() + delta.x()
                if self.m_drag_edge.Left
                else self.x()
            )
            y = (
                self.m_original_geometry.y() + delta.y()
                if self.m_drag_edge.Top
                else self.y()
            )
            width = (
                self.m_original_geometry.width() - delta.x()
                if self.m_drag_edge.Left
                else self.m_original_geometry.width() + delta.x()
                if self.m_drag_edge.Right
                else self.width()
            )
            height = (
                self.m_original_geometry.height() - delta.y()
                if self.m_drag_edge.Top
                else self.m_original_geometry.height() + delta.y()
                if self.m_drag_edge.Bottom
                else self.height()
            )
            if width < self.minimumWidth() or height < self.minimumHeight():
                return
            self.setGeometry(*[round(n * self.scaling) for n in [x, y, width, height]])
        else:
            # 窗口拖动
            new_pos = self.pos() + delta
            self.move(new_pos)
            self.m_drag_start_pos = event.globalPos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.m_drag_start_pos = None
        self.m_original_geometry = None
        self.m_drag_edge = None
        self.update_cursor_shape(event.pos())
        super().mouseReleaseEvent(event)

    def update_cursor_shape(self, pos):
        """根据鼠标位置更新光标形状"""
        edge = self.get_edge_at_position(pos)
        self.setCursor(_CursorShape.get(edge, Qt.CursorShape.ArrowCursor))

    def leaveEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)
