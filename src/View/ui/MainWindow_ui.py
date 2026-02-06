# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QToolBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1279, 719)
        self.action_locate = QAction(MainWindow)
        self.action_locate.setObjectName(u"action_locate")
        self.action_locate.setMenuRole(QAction.MenuRole.NoRole)
        self.action_preview = QAction(MainWindow)
        self.action_preview.setObjectName(u"action_preview")
        self.action_preview.setMenuRole(QAction.MenuRole.NoRole)
        self.action_capture = QAction(MainWindow)
        self.action_capture.setObjectName(u"action_capture")
        self.action_capture.setCheckable(True)
        self.action_capture.setMenuRole(QAction.MenuRole.NoRole)
        self.action_stitch = QAction(MainWindow)
        self.action_stitch.setObjectName(u"action_stitch")
        self.action_stitch.setMenuRole(QAction.MenuRole.NoRole)
        self.action_reclip = QAction(MainWindow)
        self.action_reclip.setObjectName(u"action_reclip")
        self.action_reclip.setMenuRole(QAction.MenuRole.NoRole)
        self.action_select_folder = QAction(MainWindow)
        self.action_select_folder.setObjectName(u"action_select_folder")
        self.action_select_folder.setMenuRole(QAction.MenuRole.NoRole)
        self.action_open_folder = QAction(MainWindow)
        self.action_open_folder.setObjectName(u"action_open_folder")
        self.action_open_folder.setMenuRole(QAction.MenuRole.NoRole)
        self.action_rename_folder = QAction(MainWindow)
        self.action_rename_folder.setObjectName(u"action_rename_folder")
        self.action_rename_folder.setMenuRole(QAction.MenuRole.NoRole)
        self.action_output_pdf = QAction(MainWindow)
        self.action_output_pdf.setObjectName(u"action_output_pdf")
        self.action_print_score = QAction(MainWindow)
        self.action_print_score.setObjectName(u"action_print_score")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1279, 33))
        self.menu_view = QMenu(self.menubar)
        self.menu_view.setObjectName(u"menu_view")
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName(u"menu_help")
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar_main = QToolBar(MainWindow)
        self.toolBar_main.setObjectName(u"toolBar_main")
        self.toolBar_main.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar_main)
        self.toolBar_path = QToolBar(MainWindow)
        self.toolBar_path.setObjectName(u"toolBar_path")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar_path)
        self.toolBar_view = QToolBar(MainWindow)
        self.toolBar_view.setObjectName(u"toolBar_view")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar_view)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_view.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.action_select_folder)
        self.menu_file.addAction(self.action_rename_folder)
        self.menu_file.addAction(self.action_open_folder)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_output_pdf)
        self.menu_file.addAction(self.action_print_score)
        self.menu.addAction(self.action_locate)
        self.menu.addAction(self.action_preview)
        self.menu.addAction(self.action_capture)
        self.menu.addAction(self.action_stitch)
        self.menu.addAction(self.action_reclip)
        self.toolBar_main.addSeparator()
        self.toolBar_main.addAction(self.action_locate)
        self.toolBar_main.addAction(self.action_preview)
        self.toolBar_main.addAction(self.action_capture)
        self.toolBar_main.addAction(self.action_stitch)
        self.toolBar_main.addAction(self.action_reclip)
        self.toolBar_path.addAction(self.action_select_folder)
        self.toolBar_path.addAction(self.action_rename_folder)
        self.toolBar_path.addAction(self.action_open_folder)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Score Capture", None))
        self.action_locate.setText(QCoreApplication.translate("MainWindow", u"\u5b9a\u4f4d", None))
        self.action_preview.setText(QCoreApplication.translate("MainWindow", u"\u9884\u89c8", None))
        self.action_capture.setText(QCoreApplication.translate("MainWindow", u"\u622a\u56fe", None))
        self.action_stitch.setText(QCoreApplication.translate("MainWindow", u"\u62fc\u63a5", None))
        self.action_reclip.setText(QCoreApplication.translate("MainWindow", u"\u5206\u5272", None))
        self.action_select_folder.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u76ee\u5f55", None))
        self.action_open_folder.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u76ee\u5f55", None))
#if QT_CONFIG(tooltip)
        self.action_open_folder.setToolTip(QCoreApplication.translate("MainWindow", u"\u5728\u6587\u4ef6\u8d44\u6e90\u7ba1\u7406\u5668\u4e2d\u6253\u5f00", None))
#endif // QT_CONFIG(tooltip)
        self.action_rename_folder.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u547d\u540d\u76ee\u5f55", None))
        self.action_output_pdf.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51faPDF", None))
        self.action_print_score.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5370", None))
        self.menu_view.setTitle(QCoreApplication.translate("MainWindow", u"\u89c6\u56fe", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u64cd\u4f5c", None))
        self.toolBar_main.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar_main", None))
        self.toolBar_path.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
        self.toolBar_view.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

