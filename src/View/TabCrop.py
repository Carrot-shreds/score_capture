from typing import cast

from pyqtgraph import ViewBox
from pyqtgraph import functions as fn
from pyqtgraph.GraphicsScene.mouseEvents import MouseDragEvent
from pyqtgraph.Point import Point
from pyqtgraph.Qt import QtCore
from PySide6.QtCore import QPoint, QPointF, QRectF
from PySide6.QtWidgets import QWidget

from .ui.TabCrop_ui import Ui_TabCrop


class CropViewBox(ViewBox):
    # All points mapped to image data coordinates
    regionSelected = QtCore.Signal(QRectF)
    dragStarted = QtCore.Signal(QPoint)
    dragMoved = QtCore.Signal(QPoint)
    dragFinished = QtCore.Signal(QPoint)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.draging_anchor: bool = False

    def mouseDragEvent(self, ev: MouseDragEvent, axis=None):
        ## if axis is specified, event will only affect that axis.
        ev.accept()  ## we accept all buttons

        pos = ev.pos()
        lastPos = ev.lastPos()
        dif = pos - lastPos
        dif = dif * -1

        ## Scale or translate based on mouse button
        if ev.button() in [
            QtCore.Qt.MouseButton.LeftButton,
            QtCore.Qt.MouseButton.MiddleButton,
        ]:
            point: QPoint = cast(QPointF, self.childGroup.mapFromParent(pos)).toPoint()
            if ev.isStart():
                self.dragStarted.emit(point)
            elif ev.isFinish():
                self.dragFinished.emit(point)
            else:
                self.dragMoved.emit(point)

            if self.draging_anchor:
                return  # Event already be handled in TabCrop_VM

            tr = self.childGroup.transform()
            tr = fn.invertQTransform(tr)
            tr = tr.map(dif) - tr.map(Point(0, 0))

            x, y = tr.x(), tr.y()

            self._resetTarget()
            if x is not None or y is not None:
                self.translateBy(x=x, y=y)
            self.sigRangeChangedManually.emit(self.state["mouseEnabled"])
        elif ev.button() & QtCore.Qt.MouseButton.RightButton:
            if ev.isFinish():  ## This is the final move in the drag; pass the region through the signal
                rect = QtCore.QRectF(Point(ev.buttonDownPos(ev.button())), Point(pos))
                rect = self.childGroup.mapRectFromParent(rect)
                self.rbScaleBox.hide()
                self.axHistoryPointer += 1
                self.axHistory = self.axHistory[: self.axHistoryPointer] + [rect]
                self.regionSelected.emit(rect)
            else:
                ## update shape of scale box
                self.updateScaleBox(ev.buttonDownPos(), ev.pos())


class TabCrop_View(QWidget, Ui_TabCrop):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)

        # Modify the original viewbox mouse event.
        # Replacement code from viewbox.__init__
        cropViewBox = CropViewBox()
        imageview = self.ImageViewer.imageView
        imageview.view = cropViewBox
        imageview.ui.graphicsView.setCentralItem(cropViewBox)
        cropViewBox.setAspectLocked(True)
        cropViewBox.invertY()
        cropViewBox.addItem(imageview.roi)
        cropViewBox.addItem(imageview.normRoi)
        cropViewBox.addItem(imageview.imageItem)
        for f in ["addItem", "removeItem"]:
            setattr(self, f, getattr(cropViewBox, f))
        cropViewBox.register(imageview.name)
