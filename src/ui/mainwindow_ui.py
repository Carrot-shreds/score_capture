# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFrame, QGridLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QSpinBox, QSplitter,
    QStatusBar, QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1067, 488)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_5 = QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.splitter_2 = QSplitter(self.centralwidget)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.splitter_2.setOpaqueResize(True)
        self.splitter_2.setChildrenCollapsible(False)
        self.frame_sidebar = QFrame(self.splitter_2)
        self.frame_sidebar.setObjectName(u"frame_sidebar")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_sidebar.sizePolicy().hasHeightForWidth())
        self.frame_sidebar.setSizePolicy(sizePolicy)
        self.frame_sidebar.setMinimumSize(QSize(130, 0))
        self.verticalLayout = QVBoxLayout(self.frame_sidebar)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_logo = QLabel(self.frame_sidebar)
        self.label_logo.setObjectName(u"label_logo")
        font = QFont()
        font.setPointSize(22)
        self.label_logo.setFont(font)
        self.label_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_logo)

        self.pushButton_locate = QPushButton(self.frame_sidebar)
        self.pushButton_locate.setObjectName(u"pushButton_locate")

        self.verticalLayout.addWidget(self.pushButton_locate)

        self.pushButton_preview = QPushButton(self.frame_sidebar)
        self.pushButton_preview.setObjectName(u"pushButton_preview")

        self.verticalLayout.addWidget(self.pushButton_preview)

        self.pushButton_capture = QPushButton(self.frame_sidebar)
        self.pushButton_capture.setObjectName(u"pushButton_capture")

        self.verticalLayout.addWidget(self.pushButton_capture)

        self.pushButton_stitch = QPushButton(self.frame_sidebar)
        self.pushButton_stitch.setObjectName(u"pushButton_stitch")

        self.verticalLayout.addWidget(self.pushButton_stitch)

        self.pushButton_reclip = QPushButton(self.frame_sidebar)
        self.pushButton_reclip.setObjectName(u"pushButton_reclip")

        self.verticalLayout.addWidget(self.pushButton_reclip)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.pushButton_instruction = QPushButton(self.frame_sidebar)
        self.pushButton_instruction.setObjectName(u"pushButton_instruction")

        self.verticalLayout.addWidget(self.pushButton_instruction)

        self.label_author = QLabel(self.frame_sidebar)
        self.label_author.setObjectName(u"label_author")

        self.verticalLayout.addWidget(self.label_author)

        self.splitter_2.addWidget(self.frame_sidebar)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.gridLayout_3 = QGridLayout(self.layoutWidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 7)

        self.pushButton_select_path = QPushButton(self.layoutWidget)
        self.pushButton_select_path.setObjectName(u"pushButton_select_path")

        self.gridLayout.addWidget(self.pushButton_select_path, 1, 6, 1, 1)

        self.comboBox_save_format = QComboBox(self.layoutWidget)
        self.comboBox_save_format.addItem("")
        self.comboBox_save_format.addItem("")
        self.comboBox_save_format.setObjectName(u"comboBox_save_format")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBox_save_format.sizePolicy().hasHeightForWidth())
        self.comboBox_save_format.setSizePolicy(sizePolicy1)
        self.comboBox_save_format.setMinimumSize(QSize(55, 0))

        self.gridLayout.addWidget(self.comboBox_save_format, 2, 8, 1, 1)

        self.pushButton_select_folder = QPushButton(self.layoutWidget)
        self.pushButton_select_folder.setObjectName(u"pushButton_select_folder")

        self.gridLayout.addWidget(self.pushButton_select_folder, 2, 3, 1, 1)

        self.checkBox_auto_manage_config = QCheckBox(self.layoutWidget)
        self.checkBox_auto_manage_config.setObjectName(u"checkBox_auto_manage_config")

        self.gridLayout.addWidget(self.checkBox_auto_manage_config, 1, 7, 1, 2)

        self.checkBox_always_on_top = QCheckBox(self.layoutWidget)
        self.checkBox_always_on_top.setObjectName(u"checkBox_always_on_top")

        self.gridLayout.addWidget(self.checkBox_always_on_top, 0, 7, 1, 2)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.lineEdit_save_path = QLineEdit(self.layoutWidget)
        self.lineEdit_save_path.setObjectName(u"lineEdit_save_path")

        self.gridLayout.addWidget(self.lineEdit_save_path, 1, 1, 1, 5)

        self.label_12 = QLabel(self.layoutWidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_12, 2, 5, 1, 1)

        self.pushButton_open_folder = QPushButton(self.layoutWidget)
        self.pushButton_open_folder.setObjectName(u"pushButton_open_folder")

        self.gridLayout.addWidget(self.pushButton_open_folder, 2, 4, 1, 1)

        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.lineEdit_score_title = QLineEdit(self.layoutWidget)
        self.lineEdit_score_title.setObjectName(u"lineEdit_score_title")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEdit_score_title.sizePolicy().hasHeightForWidth())
        self.lineEdit_score_title.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.lineEdit_score_title, 2, 1, 1, 1)

        self.label_6 = QLabel(self.layoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 2, 7, 1, 1)

        self.comboBox_log_level = QComboBox(self.layoutWidget)
        self.comboBox_log_level.addItem("")
        self.comboBox_log_level.addItem("")
        self.comboBox_log_level.addItem("")
        self.comboBox_log_level.addItem("")
        self.comboBox_log_level.addItem("")
        self.comboBox_log_level.setObjectName(u"comboBox_log_level")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.comboBox_log_level.sizePolicy().hasHeightForWidth())
        self.comboBox_log_level.setSizePolicy(sizePolicy3)
        self.comboBox_log_level.setMinimumSize(QSize(90, 0))

        self.gridLayout.addWidget(self.comboBox_log_level, 2, 6, 1, 1)

        self.pushButton_rename_folder = QPushButton(self.layoutWidget)
        self.pushButton_rename_folder.setObjectName(u"pushButton_rename_folder")
        sizePolicy3.setHeightForWidth(self.pushButton_rename_folder.sizePolicy().hasHeightForWidth())
        self.pushButton_rename_folder.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.pushButton_rename_folder, 2, 2, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_10 = QLabel(self.layoutWidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_10, 0, 5, 1, 4)

        self.spinBox_region_height = QSpinBox(self.layoutWidget)
        self.spinBox_region_height.setObjectName(u"spinBox_region_height")
        sizePolicy3.setHeightForWidth(self.spinBox_region_height.sizePolicy().hasHeightForWidth())
        self.spinBox_region_height.setSizePolicy(sizePolicy3)
        self.spinBox_region_height.setMinimumSize(QSize(80, 0))
        self.spinBox_region_height.setMaximum(2000)

        self.gridLayout_4.addWidget(self.spinBox_region_height, 2, 8, 1, 1)

        self.checkBox_reverse_image = QCheckBox(self.layoutWidget)
        self.checkBox_reverse_image.setObjectName(u"checkBox_reverse_image")

        self.gridLayout_4.addWidget(self.checkBox_reverse_image, 2, 1, 1, 1)

        self.checkBox_keep_last = QCheckBox(self.layoutWidget)
        self.checkBox_keep_last.setObjectName(u"checkBox_keep_last")

        self.gridLayout_4.addWidget(self.checkBox_keep_last, 2, 0, 1, 1)

        self.label_7 = QLabel(self.layoutWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_7, 2, 5, 1, 1)

        self.label_14 = QLabel(self.layoutWidget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_14, 1, 0, 1, 1)

        self.label_8 = QLabel(self.layoutWidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_8, 2, 7, 1, 1)

        self.label_13 = QLabel(self.layoutWidget)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_4.addWidget(self.label_13, 2, 2, 1, 1)

        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.comboBox_clip_align = QComboBox(self.layoutWidget)
        self.comboBox_clip_align.addItem("")
        self.comboBox_clip_align.addItem("")
        self.comboBox_clip_align.addItem("")
        self.comboBox_clip_align.setObjectName(u"comboBox_clip_align")

        self.gridLayout_6.addWidget(self.comboBox_clip_align, 4, 9, 1, 1)

        self.label_25 = QLabel(self.layoutWidget)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_25, 0, 8, 1, 2)

        self.radioButton_stitch_direction_vertical = QRadioButton(self.layoutWidget)
        self.radioButton_stitch_direction_vertical.setObjectName(u"radioButton_stitch_direction_vertical")

        self.gridLayout_6.addWidget(self.radioButton_stitch_direction_vertical, 4, 4, 1, 1)

        self.comboBox_stitch_method = QComboBox(self.layoutWidget)
        self.comboBox_stitch_method.addItem("")
        self.comboBox_stitch_method.addItem("")
        self.comboBox_stitch_method.addItem("")
        self.comboBox_stitch_method.setObjectName(u"comboBox_stitch_method")
        sizePolicy3.setHeightForWidth(self.comboBox_stitch_method.sizePolicy().hasHeightForWidth())
        self.comboBox_stitch_method.setSizePolicy(sizePolicy3)

        self.gridLayout_6.addWidget(self.comboBox_stitch_method, 1, 4, 1, 2)

        self.comboBox_reclip_method = QComboBox(self.layoutWidget)
        self.comboBox_reclip_method.addItem("")
        self.comboBox_reclip_method.addItem("")
        self.comboBox_reclip_method.setObjectName(u"comboBox_reclip_method")

        self.gridLayout_6.addWidget(self.comboBox_reclip_method, 1, 9, 1, 1)

        self.label_17 = QLabel(self.layoutWidget)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_17, 1, 3, 1, 1)

        self.label_18 = QLabel(self.layoutWidget)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_18, 1, 8, 1, 1)

        self.label_27 = QLabel(self.layoutWidget)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_27, 4, 3, 1, 1)

        self.radioButton_stitch_direction_horizontal = QRadioButton(self.layoutWidget)
        self.radioButton_stitch_direction_horizontal.setObjectName(u"radioButton_stitch_direction_horizontal")

        self.gridLayout_6.addWidget(self.radioButton_stitch_direction_horizontal, 4, 5, 1, 1)

        self.label_24 = QLabel(self.layoutWidget)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_24, 0, 3, 1, 3)

        self.label_19 = QLabel(self.layoutWidget)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_19.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_19, 4, 8, 1, 1)

        self.label_31 = QLabel(self.layoutWidget)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_31, 0, 1, 1, 2)

        self.label_30 = QLabel(self.layoutWidget)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_30, 1, 1, 1, 1)

        self.label_33 = QLabel(self.layoutWidget)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_33, 4, 1, 1, 1)

        self.doubleSpinBox_detect_coefficient_horizontal = QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBox_detect_coefficient_horizontal.setObjectName(u"doubleSpinBox_detect_coefficient_horizontal")
        self.doubleSpinBox_detect_coefficient_horizontal.setMaximum(65535.000000000000000)
        self.doubleSpinBox_detect_coefficient_horizontal.setSingleStep(0.100000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_detect_coefficient_horizontal, 1, 2, 1, 1)

        self.doubleSpinBox_detect_coefficient_vertical = QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBox_detect_coefficient_vertical.setObjectName(u"doubleSpinBox_detect_coefficient_vertical")
        self.doubleSpinBox_detect_coefficient_vertical.setMaximum(65535.000000000000000)
        self.doubleSpinBox_detect_coefficient_vertical.setSingleStep(0.100000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_detect_coefficient_vertical, 4, 2, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_6, 3, 0, 1, 9)

        self.label_9 = QLabel(self.layoutWidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_9, 1, 5, 1, 1)

        self.doubleSpinBox_compare_threshold = QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBox_compare_threshold.setObjectName(u"doubleSpinBox_compare_threshold")
        self.doubleSpinBox_compare_threshold.setMaximum(65535.000000000000000)
        self.doubleSpinBox_compare_threshold.setSingleStep(0.100000000000000)

        self.gridLayout_4.addWidget(self.doubleSpinBox_compare_threshold, 1, 3, 1, 1)

        self.comboBox_compare_method = QComboBox(self.layoutWidget)
        self.comboBox_compare_method.addItem("")
        self.comboBox_compare_method.addItem("")
        self.comboBox_compare_method.setObjectName(u"comboBox_compare_method")

        self.gridLayout_4.addWidget(self.comboBox_compare_method, 1, 1, 1, 1)

        self.spinBox_region_y = QSpinBox(self.layoutWidget)
        self.spinBox_region_y.setObjectName(u"spinBox_region_y")
        sizePolicy3.setHeightForWidth(self.spinBox_region_y.sizePolicy().hasHeightForWidth())
        self.spinBox_region_y.setSizePolicy(sizePolicy3)
        self.spinBox_region_y.setMinimumSize(QSize(80, 0))
        self.spinBox_region_y.setMaximum(2000)

        self.gridLayout_4.addWidget(self.spinBox_region_y, 1, 8, 1, 1)

        self.label_16 = QLabel(self.layoutWidget)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_4.addWidget(self.label_16, 1, 2, 1, 1)

        self.doubleSpinBox_capture_delay = QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBox_capture_delay.setObjectName(u"doubleSpinBox_capture_delay")
        self.doubleSpinBox_capture_delay.setSingleStep(0.100000000000000)

        self.gridLayout_4.addWidget(self.doubleSpinBox_capture_delay, 2, 3, 1, 1)

        self.label_11 = QLabel(self.layoutWidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_11, 1, 7, 1, 1)

        self.spinBox_region_x = QSpinBox(self.layoutWidget)
        self.spinBox_region_x.setObjectName(u"spinBox_region_x")
        sizePolicy3.setHeightForWidth(self.spinBox_region_x.sizePolicy().hasHeightForWidth())
        self.spinBox_region_x.setSizePolicy(sizePolicy3)
        self.spinBox_region_x.setMinimumSize(QSize(80, 0))
        self.spinBox_region_x.setMaximum(2000)

        self.gridLayout_4.addWidget(self.spinBox_region_x, 1, 6, 1, 1)

        self.spinBox_region_width = QSpinBox(self.layoutWidget)
        self.spinBox_region_width.setObjectName(u"spinBox_region_width")
        sizePolicy3.setHeightForWidth(self.spinBox_region_width.sizePolicy().hasHeightForWidth())
        self.spinBox_region_width.setSizePolicy(sizePolicy3)
        self.spinBox_region_width.setMinimumSize(QSize(80, 0))
        self.spinBox_region_width.setMaximum(2000)

        self.gridLayout_4.addWidget(self.spinBox_region_width, 2, 6, 1, 1)

        self.label_15 = QLabel(self.layoutWidget)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_15, 0, 0, 1, 5)

        self.pushButton_image_rebuild = QPushButton(self.layoutWidget)
        self.pushButton_image_rebuild.setObjectName(u"pushButton_image_rebuild")

        self.gridLayout_4.addWidget(self.pushButton_image_rebuild, 1, 4, 1, 1)

        self.pushButton_image_reorder = QPushButton(self.layoutWidget)
        self.pushButton_image_reorder.setObjectName(u"pushButton_image_reorder")

        self.gridLayout_4.addWidget(self.pushButton_image_reorder, 2, 4, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_4, 1, 0, 1, 2)

        self.splitter.addWidget(self.layoutWidget)
        self.textEdit_console = QTextEdit(self.splitter)
        self.textEdit_console.setObjectName(u"textEdit_console")
        self.splitter.addWidget(self.textEdit_console)
        self.splitter_2.addWidget(self.splitter)

        self.gridLayout_5.addWidget(self.splitter_2, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1067, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Score Capture", None))
        self.label_logo.setText(QCoreApplication.translate("MainWindow", u"Score\n"
"Capture", None))
        self.pushButton_locate.setText(QCoreApplication.translate("MainWindow", u"\u5b9a\u4f4d", None))
        self.pushButton_preview.setText(QCoreApplication.translate("MainWindow", u"\u9884\u89c8", None))
        self.pushButton_capture.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u622a\u56fe", None))
        self.pushButton_stitch.setText(QCoreApplication.translate("MainWindow", u"\u62fc\u63a5", None))
        self.pushButton_reclip.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u5206\u5272", None))
        self.pushButton_instruction.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u8bf4\u660e\u6587\u6863", None))
        self.label_author.setText(QCoreApplication.translate("MainWindow", u"Carrot shreds", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u5168\u5c40\u8bbe\u7f6e", None))
        self.pushButton_select_path.setText(QCoreApplication.translate("MainWindow", u"\u6d4f\u89c8\u76ee\u5f55", None))
        self.comboBox_save_format.setItemText(0, QCoreApplication.translate("MainWindow", u".jpg", None))
        self.comboBox_save_format.setItemText(1, QCoreApplication.translate("MainWindow", u".png", None))

        self.pushButton_select_folder.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.checkBox_auto_manage_config.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u4fdd\u5b58/\u52a0\u8f7d\u914d\u7f6e", None))
        self.checkBox_always_on_top.setText(QCoreApplication.translate("MainWindow", u"\u7a97\u53e3\u59cb\u7ec8\u9760\u524d", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u66f2\u8c31\u6807\u9898\uff1a", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u65e5\u5fd7\u7b49\u7ea7\uff1a", None))
        self.pushButton_open_folder.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u76ee\u5f55", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u5b58\u50a8\u8def\u5f84\uff1a", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u5b58\u50a8\u683c\u5f0f\uff1a", None))
        self.comboBox_log_level.setItemText(0, QCoreApplication.translate("MainWindow", u"DEBUG", None))
        self.comboBox_log_level.setItemText(1, QCoreApplication.translate("MainWindow", u"INFO", None))
        self.comboBox_log_level.setItemText(2, QCoreApplication.translate("MainWindow", u"SUCCESS", None))
        self.comboBox_log_level.setItemText(3, QCoreApplication.translate("MainWindow", u"WARNING", None))
        self.comboBox_log_level.setItemText(4, QCoreApplication.translate("MainWindow", u"ERROR", None))

        self.pushButton_rename_folder.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u547d\u540d", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u5b9a\u4f4d\u8bbe\u7f6e", None))
        self.checkBox_reverse_image.setText(QCoreApplication.translate("MainWindow", u"\u5bf9\u56fe\u7247\u8fdb\u884c\u53cd\u76f8", None))
        self.checkBox_keep_last.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u7559\u6700\u540e\u4e00\u7ec4\u622a\u56fe", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u5bbd:", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u6bd4\u8f83\u7b97\u6cd5\uff1a", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u9ad8:", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u622a\u56fe\u95f4\u9694(\u79d2/s)\uff1a", None))
        self.comboBox_clip_align.setItemText(0, QCoreApplication.translate("MainWindow", u"\u5c45\u5de6", None))
        self.comboBox_clip_align.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5c45\u4e2d", None))
        self.comboBox_clip_align.setItemText(2, QCoreApplication.translate("MainWindow", u"\u5c45\u53f3", None))

        self.comboBox_clip_align.setCurrentText(QCoreApplication.translate("MainWindow", u"\u5c45\u5de6", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u5206\u5272\u8bbe\u7f6e", None))
        self.radioButton_stitch_direction_vertical.setText(QCoreApplication.translate("MainWindow", u"\u7eb5\u5411", None))
        self.comboBox_stitch_method.setItemText(0, QCoreApplication.translate("MainWindow", u"MSE", None))
        self.comboBox_stitch_method.setItemText(1, QCoreApplication.translate("MainWindow", u"SSIM", None))
        self.comboBox_stitch_method.setItemText(2, QCoreApplication.translate("MainWindow", u"DIRECT", None))

        self.comboBox_stitch_method.setCurrentText(QCoreApplication.translate("MainWindow", u"MSE", None))
        self.comboBox_reclip_method.setItemText(0, QCoreApplication.translate("MainWindow", u"\u56fa\u5b9a\u5c0f\u8282", None))
        self.comboBox_reclip_method.setItemText(1, QCoreApplication.translate("MainWindow", u"\u9650\u5236\u5bbd\u5ea6", None))

        self.comboBox_reclip_method.setCurrentText(QCoreApplication.translate("MainWindow", u"\u56fa\u5b9a\u5c0f\u8282", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"\u62fc\u63a5\u70b9\u7b97\u6cd5\uff1a", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"\u5206\u5272\u6a21\u5f0f\uff1a", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"\u62fc\u63a5\u65b9\u5411\uff1a", None))
        self.radioButton_stitch_direction_horizontal.setText(QCoreApplication.translate("MainWindow", u"\u6a2a\u5411", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u50cf\u62fc\u63a5\u8bbe\u7f6e", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"\u5207\u7247\u5bf9\u9f50\uff1a", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"\u68c0\u6d4b\u7b97\u6cd5\u8bbe\u7f6e", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"\u6c34\u5e73\u7ebf\u6bb5\u7cfb\u6570", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"\u7ad6\u76f4\u7ebf\u6bb5\u7cfb\u6570", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"X:", None))
        self.comboBox_compare_method.setItemText(0, QCoreApplication.translate("MainWindow", u"SSIM", None))
        self.comboBox_compare_method.setItemText(1, QCoreApplication.translate("MainWindow", u"MSE", None))

        self.label_16.setText(QCoreApplication.translate("MainWindow", u"\u622a\u81f3\u5dee\u5f02\u503c\uff1a", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Y:", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"\u622a\u56fe\u8bbe\u7f6e", None))
        self.pushButton_image_rebuild.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u6784\u5efaimage", None))
        self.pushButton_image_reorder.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u7f16\u53f7image", None))
    # retranslateUi

