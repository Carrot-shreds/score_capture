from PySide6.QtWidgets import QWidget

from .ui.TabStitch_ui import Ui_TabStitch


class TabStitch_View(QWidget, Ui_TabStitch):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)
