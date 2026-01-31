from typing import NamedTuple, TypedDict

from PySide6.QtCore import QPoint, QRect, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QDialog, QPushButton

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
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # 去掉默认边框

        # 自定义边框鼠标事件
        self.m_drag_start_pos: QPoint | None = None
        self.m_original_geometry: QRect | None = None
        self.m_drag_edge: EdgeTuple | None = None
        self.m_resize_margin: int = 12  # 边缘检测范围
        self.setMouseTracking(True)

        self.pushButton_toggle_show_mode = QPushButton(self)
        self.pushButton_toggle_show_mode.setGeometry(3, 3, 20, 20)
        self.pushButton_toggle_show_mode.setText("—")

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
        if event.button() == Qt.MouseButton.RightButton:
            self.showMinimized()

    def mouseMoveEvent(self, event: QMouseEvent):
        self.update_cursor_shape(event.pos())
        if not self.m_drag_start_pos or not self.m_original_geometry:
            return

        delta = event.globalPos() - self.m_drag_start_pos

        if self.m_drag_edge and any(self.m_drag_edge):
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
            self.setGeometry(x, y, width, height)
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
