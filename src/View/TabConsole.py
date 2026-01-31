from PySide6.QtWidgets import QWidget

from .ui.TabConsole_ui import Ui_TabConsole


class TabConsole_View(QWidget, Ui_TabConsole):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)
