from PySide6.QtWidgets import QWidget

from .ui.TabSettings_ui import Ui_TabSettings


class TabSettings_View(QWidget, Ui_TabSettings):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)
