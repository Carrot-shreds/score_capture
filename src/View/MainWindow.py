import PySide6QtAds as QtAds
from PySide6.QtCore import QSignalBlocker, Qt
from PySide6.QtGui import QAction, QCloseEvent, QKeySequence
from PySide6.QtWidgets import (
    QComboBox,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
    QWidgetAction,
)

from .ui.MainWindow_ui import Ui_MainWindow


class MainWindow_View(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        # tool bar
        self.toolBar_path.clear()
        self.lineEdit_score_title = QLineEdit(self)
        self.toolBar_path.addSeparator()
        self.toolBar_path.addWidget(QLabel("标题:"))
        self.toolBar_path.addWidget(self.lineEdit_score_title)
        self.toolBar_path.addAction(self.action_select_folder)
        self.toolBar_path.addAction(self.action_rename_folder)
        self.toolBar_path.addAction(self.action_open_folder)
        self.action_mainwindow_always_top = QAction("置顶窗口")
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

        # status bar
        self.label_version = QLabel()
        self.label_version.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.statusbar.addPermanentWidget(self.label_version)  # 从右往左添加
        self.statusbar.addWidget(QLabel("    "))
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
        dock_widget_settings = self.dock_manager.createDockWidget("Settings")
        dock_widget_settings.setWidget(tab_settings)
        dock_area_settings = self.dock_manager.addAutoHideDockWidget(
            QtAds.SideBarLeft, dock_widget_settings
        )
        dock_area_settings.setSize(self.frameGeometry().width() * 2 // 3)
        # Console
        dock_widget_console = self.dock_manager.createDockWidget("Console")
        dock_widget_console.setWidget(tab_console)
        dock_area_console = self.dock_manager.addDockWidget(  # noqa:F841
            QtAds.BottomDockWidgetArea, dock_widget_console
        )
        # Preview
        dock_widget_preview = self.dock_manager.createDockWidget("Preview")
        dock_widget_preview.setWidget(tab_preview)
        self.dock_manager.addDockWidgetTabToArea(dock_widget_preview, dock_area_central)
        # Stitch
        self.dock_widget_stitch = self.dock_manager.createDockWidget("Stitch")
        self.dock_widget_stitch.setWidget(tab_stitch)
        self.dock_manager.addDockWidgetTabToArea(
            self.dock_widget_stitch, dock_area_central
        )
        # Reclip
        dock_widget_reclip = self.dock_manager.createDockWidget("Reclip")
        dock_widget_reclip.setWidget(tab_reclip)
        self.dock_manager.addDockWidgetTabToArea(dock_widget_reclip, dock_area_central)
        dock_area_central.setCurrentDockWidget(dock_widget_preview)

        # Add actions
        self.menu_view.addAction(dock_widget_console.toggleViewAction())
        self.menu_view.addAction(dock_widget_settings.toggleViewAction())
        self.menu_view.addAction(dock_widget_preview.toggleViewAction())
        self.menu_view.addAction(self.dock_widget_stitch.toggleViewAction())
        self.menu_view.addAction(dock_widget_reclip.toggleViewAction())

        # Add docking perspective select
        self.create_docking_perspective()
        # add default perspective
        if "default" not in self.dock_manager.perspectiveNames():
            self.new_docking_perspective("default")

    def create_docking_perspective(self):
        save_perspective_action = QAction("保存当前", self)
        save_perspective_action.triggered.connect(self.handel_new_docking_perspective)
        remove_perspective_action = QAction("删除当前", self)
        remove_perspective_action.triggered.connect(self.remove_docking_perspective)
        perspective_list_action = QWidgetAction(self)
        self.perspective_combobox = QComboBox(self)
        self.perspective_combobox.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToContents
        )
        self.perspective_combobox.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        self.perspective_combobox.textActivated.connect(
            self.dock_manager.openPerspective
        )
        perspective_list_action.setDefaultWidget(self.perspective_combobox)
        self.toolBar_view.addSeparator()
        self.toolBar_view.addWidget(QLabel("布局预设:"))
        self.toolBar_view.addAction(perspective_list_action)
        self.toolBar_view.addAction(save_perspective_action)
        self.toolBar_view.addAction(remove_perspective_action)
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
            self, "保存视图预设", "请输入唯一识别名称："
        )
        if not ok or not perspective_name:
            return
        self.new_docking_perspective(perspective_name)

    def closeEvent(self, event: QCloseEvent):
        self.dock_manager.deleteLater()
        super().closeEvent(event)
