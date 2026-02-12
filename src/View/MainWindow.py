import time

import PySide6QtAds as QtAds
from PySide6.QtCore import QFile, QIODevice, QSignalBlocker, Qt
from PySide6.QtGui import (
    QAction,
    QCloseEvent,
    QDesktopServices,
    QKeySequence,
    QMouseEvent,
    QShortcut,
)
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QWidgetAction,
)

from .ui.MainWindow_ui import Ui_MainWindow

LANGUAGES: dict[str, str] = {"English": "en", "简体中文": "zh_CN"}


class GPLLabel(QLabel):
    def __init__(self):
        super().__init__("Free software under GPLv3")
        self.click_times: int = 0
        self.start_time: int = 0

    def play(self):
        pass

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self.click_times += 1
        if self.start_time == 0:
            self.start_time = int(time.time())
        elif int(time.time()) - self.start_time > 3:
            self.click_times = 0
            self.start_time = 0
        elif self.click_times >= 7:
            self.play()
            self.click_times = 0
            self.start_time = 0


class About(QDialog):
    def __init__(self, parent, version: str) -> None:
        super().__init__(parent)
        self.setWindowTitle(self.tr("About"))
        self.label_title = QLabel("Score capture")
        self.label_version = QLabel(f"Version: {version}")
        self.label_copyright = QLabel("Copyright © 2025 Carrot-shreds")
        self.label_repo = QLabel(
            "<a href='https://github.com/Carrot-shreds/score_capture'>Open source repository</a>",
            openExternalLinks=True,
        )
        self.button_license = QPushButton(self.tr("View license"))
        self.button_license.clicked.connect(lambda: License(self))
        self.label_gpl = GPLLabel()

        self.boxlayout = QVBoxLayout(self)
        self.boxlayout.addWidget(self.label_title)
        self.boxlayout.addWidget(self.label_version)
        self.boxlayout.addWidget(self.label_copyright)
        self.boxlayout.addWidget(self.label_repo)
        self.boxlayout.addWidget(self.label_gpl)
        self.boxlayout.addWidget(self.button_license)
        self.show()
        self.setFixedSize(self.size())


class License(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setWindowTitle(self.tr("License"))
        self.resize(550, 600)

        license_file = QFile(":/license")
        license_file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text)
        license_str = license_file.readAll().toStdString()
        license_file.close()

        self.license = QTextEdit()
        self.license.setText(license_str)
        self.license.setReadOnly(True)
        self.vboxlayout = QVBoxLayout(self)
        self.vboxlayout.addWidget(self.license)
        self.show()


class MainWindow_View(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.actionManual.triggered.connect(
            lambda: QDesktopServices().openUrl(
                "https://github.com/Carrot-shreds/score_capture"
            )
        )

        # tool bar
        self.toolBar_path.clear()
        self.lineEdit_score_title = QLineEdit(self)
        self.lineEdit_score_title.setToolTip(
            self.tr("Also used as title of files and score.")
        )
        self.toolBar_path.addSeparator()
        self.toolBar_path.addWidget(QLabel(self.tr("Folder Title:")))
        self.toolBar_path.addWidget(self.lineEdit_score_title)
        self.toolBar_path.addAction(self.action_select_folder)
        self.toolBar_path.addAction(self.action_rename_folder)
        self.toolBar_path.addAction(self.action_open_folder)
        self.action_mainwindow_always_top = QAction(self.tr("Always on Top"))
        self.action_mainwindow_always_top.setCheckable(True)

        # shortcut
        self.action_locate.setShortcut(QKeySequence("F1"))
        self.action_preview.setShortcut(QKeySequence("F2"))
        self.action_capture.setShortcut(QKeySequence("F3"))
        self.action_stitch.setShortcut(QKeySequence("F4"))
        self.action_reclip.setShortcut(QKeySequence("F5"))
        self.action_select_folder.setShortcut(QKeySequence.StandardKey.Open)
        self.action_rename_folder.setShortcut(QKeySequence("Ctrl+r"))
        self.action_mainwindow_always_top.setShortcut(QKeySequence("F12"))
        self.action_print_score.setShortcut(QKeySequence.StandardKey.Print)
        perspective_shortcut = [QShortcut(self) for i in range(9)]
        for i, k in enumerate(perspective_shortcut):
            k.setKey(QKeySequence(f"ctrl+{i + 1}"))
            k.activated.connect(
                lambda s=i: self.perspective_combobox.setCurrentText(
                    self.perspective_combobox.itemText(s)
                )
                if s < self.perspective_combobox.count()
                else None
            )

        # status bar
        self.label_version = QLabel()
        self.label_version.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.statusbar.addPermanentWidget(self.label_version)  # 从右往左添加
        self.statusbar.addWidget(QLabel(self.tr("      Working Dir:")))
        self.label_working_dir = QLabel()
        self.label_working_dir.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.statusbar.addWidget(self.label_working_dir)

        # Configure Qt-Advanced-Docking-System
        QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.OpaqueSplitterResize, True)
        QtAds.CDockManager.setConfigFlag(
            QtAds.CDockManager.XmlCompressionEnabled, False
        )
        QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.FocusHighlighting, True)
        QtAds.CDockManager.setAutoHideConfigFlags(
            QtAds.CDockManager.DefaultAutoHideConfig
        )
        # QtAds.CDockManager.setAutoHideConfigFlag(
        #     QtAds.CDockManager.AutoHideShowOnMouseOver, True
        # )
        self.dock_manager = QtAds.CDockManager(self)

    def create_docking_system(
        self,
        tab_console: QWidget,
        tab_settings: QWidget,
        tab_preview: QWidget,
        tab_stitch: QWidget,
        tab_reclip: QWidget,
    ) -> None:
        # Central Widget
        central_widget = QWidget()
        layout_central_label = QVBoxLayout(central_widget)
        layout_central_label.addItem(
            QSpacerItem(
                10, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )
        layout_central_label.addWidget(
            QLabel("""Score Capture""", alignment=Qt.AlignmentFlag.AlignCenter)
        )
        # layout_central_label.addWidget(
        #     QLabel("""By Carrot shreds""", alignment=Qt.AlignmentFlag.AlignCenter)
        # )
        layout_central_label.addWidget(
            QLabel(
                """Free for every music lover""", alignment=Qt.AlignmentFlag.AlignCenter
            )
        )
        layout_central_label.addWidget(
            QLabel(
                """<a href='https://github.com/Carrot-shreds/score_capture'>Open source repo</a>""",
                alignment=Qt.AlignmentFlag.AlignCenter,
                openExternalLinks=True,
            )
        )
        layout_central_label.addItem(
            QSpacerItem(
                10, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )
        dock_widget_central = self.dock_manager.createDockWidget("Central")
        dock_widget_central.setWidget(central_widget)
        dock_widget_central.setFeature(QtAds.CDockWidget.NoTab, True)
        dock_area_central = self.dock_manager.setCentralWidget(dock_widget_central)

        # Create Docking Widget and tabs
        # Settings
        dock_widget_settings = self.dock_manager.createDockWidget(self.tr("Settings"))
        dock_widget_settings.setWidget(tab_settings)
        dock_widget_settings.setObjectName(
            "Settings"
        )  # Obj name without tr for perspective saving
        dock_area_settings = self.dock_manager.addAutoHideDockWidget(
            QtAds.SideBarLeft, dock_widget_settings
        )
        dock_area_settings.setSize(self.frameGeometry().width() * 4 // 5)
        # Console
        dock_widget_console = self.dock_manager.createDockWidget(self.tr("Console"))
        dock_widget_console.setWidget(tab_console)
        dock_widget_console.setObjectName("Console")
        dock_area_console = self.dock_manager.addDockWidget(  # noqa:F841
            QtAds.BottomDockWidgetArea, dock_widget_console
        )
        # Preview
        dock_widget_preview = self.dock_manager.createDockWidget(self.tr("Preview"))
        dock_widget_preview.setWidget(tab_preview)
        dock_widget_preview.setObjectName("Preview")
        self.dock_manager.addDockWidgetTabToArea(dock_widget_preview, dock_area_central)
        # Stitch
        self.dock_widget_stitch = self.dock_manager.createDockWidget(self.tr("Stitch"))
        self.dock_widget_stitch.setWidget(tab_stitch)
        self.dock_widget_stitch.setObjectName("Stitch")
        self.dock_manager.addDockWidgetTabToArea(
            self.dock_widget_stitch, dock_area_central
        )
        # Reclip
        dock_widget_reclip = self.dock_manager.createDockWidget(self.tr("Reclip"))
        dock_widget_reclip.setWidget(tab_reclip)
        dock_widget_reclip.setObjectName("Reclip")
        self.dock_manager.addDockWidgetTabToArea(dock_widget_reclip, dock_area_central)
        dock_area_central.setCurrentDockWidget(dock_widget_preview)

        # Add actions
        self.menu_view.addAction(dock_widget_console.toggleViewAction())
        self.menu_view.addAction(dock_widget_settings.toggleViewAction())
        self.menu_view.addAction(dock_widget_preview.toggleViewAction())
        self.menu_view.addAction(self.dock_widget_stitch.toggleViewAction())
        self.menu_view.addAction(dock_widget_reclip.toggleViewAction())
        self.menu_view.addSeparator()

        # Add docking perspective select
        self.create_docking_perspective()
        self.menu_view.addAction(self.action_mainwindow_always_top)
        # add default perspective
        if "default" not in self.dock_manager.perspectiveNames():
            self.new_docking_perspective("default")

    def create_docking_perspective(self):
        save_perspective_action = QAction(self.tr("Save"), self)
        save_perspective_action.triggered.connect(self.handel_new_docking_perspective)
        remove_perspective_action = QAction(self.tr("Delete"), self)
        remove_perspective_action.triggered.connect(self.remove_docking_perspective)
        perspective_list_action = QWidgetAction(self)
        self.perspective_combobox = QComboBox(self)
        self.perspective_combobox.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToContents
        )
        self.perspective_combobox.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        self.perspective_combobox.currentTextChanged.connect(
            self.dock_manager.openPerspective
        )
        perspective_list_action.setDefaultWidget(self.perspective_combobox)

        perspective_list_action.setToolTip(self.tr("Docking system view preset."))
        save_perspective_action.setToolTip(self.tr("Save current layout"))
        remove_perspective_action.setToolTip(self.tr("Delete current using preset"))

        self.toolBar_view.addSeparator()
        self.toolBar_view.addWidget(QLabel(self.tr("Docking Perspective:")))
        self.toolBar_view.addAction(perspective_list_action)
        self.toolBar_view.addAction(save_perspective_action)
        self.toolBar_view.addAction(remove_perspective_action)
        self.toolBar_view.addSeparator()
        self.toolBar_view.addAction(self.action_mainwindow_always_top)

    def remove_docking_perspective(self):
        name = self.perspective_combobox.currentText()
        if name == "default" or name not in self.dock_manager.perspectiveNames():
            return
        self.dock_manager.removePerspective(name)
        self.perspective_combobox.clear()
        self.perspective_combobox.addItems(self.dock_manager.perspectiveNames())
        self.perspective_combobox.setCurrentText("default")

    def new_docking_perspective(self, perspective_name: str):
        self.dock_manager.addPerspective(perspective_name)
        _ = QSignalBlocker(
            self.perspective_combobox
        )  # block combobox's signal during this func below
        self.perspective_combobox.clear()
        self.perspective_combobox.addItems(self.dock_manager.perspectiveNames())
        self.perspective_combobox.setCurrentText(perspective_name)

    def handel_new_docking_perspective(self):
        perspective_name, ok = QInputDialog.getText(
            self,
            self.tr("Save docking perspective"),
            self.tr("Please input a unique name:"),
        )
        if not ok or not perspective_name:
            return
        self.new_docking_perspective(perspective_name)

    def closeEvent(self, event: QCloseEvent):
        self.dock_manager.deleteLater()
        super().closeEvent(event)
