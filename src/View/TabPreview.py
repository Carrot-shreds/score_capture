from pyqtgraph.Qt.QtWidgets import QComboBox
from PySide6 import QtCore
from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QWidget,
)

from .ui.TabPreview_ui import Ui_TabPreview


class DialogGlobImage(QDialog):
    def __init__(self, /, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowFlag(
            QtCore.Qt.WindowType.WindowStaysOnTopHint, True
        )  # 置顶，必要
        self.setWindowTitle("Glob Images")
        self.resize(400, 100)

        self.label_path = QLabel(self, text="Path:")
        self.label_path.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.lineEdit_path = QLineEdit(self)
        self.label_glob = QLabel(self, text="Glob:")
        self.label_glob.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.pushButton_select_path = QPushButton(self)
        self.pushButton_select_path.setText("Select")
        self.pushButton_ok = QPushButton(self)
        self.pushButton_ok.setText("OK")
        self.comboBox_glob = QComboBox(self)
        self.comboBox_glob.setEditable(True)
        self.comboBox_glob.addItem("image*[!a-z].*")
        self.comboBox_glob.addItem("capture*")
        self.comboBox_glob.addItem("*stitched")
        self.comboBox_glob.addItem("image*")

        layout_grid = QGridLayout(self)
        layout_grid.addWidget(self.label_path, 1, 1, 1, 1)
        layout_grid.addWidget(self.lineEdit_path, 1, 2, 1, 2)
        layout_grid.addWidget(self.pushButton_select_path, 1, 4, 1, 1)
        layout_grid.addWidget(self.label_glob, 2, 1, 1, 1)
        layout_grid.addWidget(self.comboBox_glob, 2, 2, 1, 2)
        layout_grid.addWidget(self.pushButton_ok, 2, 4, 1, 1)

        self.pushButton_ok.setFocus()


class TabPreview_View(QWidget, Ui_TabPreview):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)

    def create_glob_dialog(self) -> DialogGlobImage:
        dialog = DialogGlobImage(self)
        return dialog
