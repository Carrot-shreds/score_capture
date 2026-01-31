from PySide6.QtWidgets import QWidget

from .ui.TabReclip_ui import Ui_TabReclip


class TabReclip_View(QWidget, Ui_TabReclip):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)

        self.scrollArea.resize(200, 300)
