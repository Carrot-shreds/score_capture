# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TabSettings.ui'
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
    QFrame, QGridLayout, QGroupBox, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_TabSettings(object):
    def setupUi(self, TabSettings):
        if not TabSettings.objectName():
            TabSettings.setObjectName(u"TabSettings")
        TabSettings.resize(901, 568)
        self.verticalLayout = QVBoxLayout(TabSettings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(TabSettings)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 881, 548))
        self.gridLayout_3 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_4 = QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.pushButton_select_folder = QPushButton(self.groupBox_3)
        self.pushButton_select_folder.setObjectName(u"pushButton_select_folder")

        self.gridLayout_4.addWidget(self.pushButton_select_folder, 3, 3, 1, 1)

        self.pushButton_select_path = QPushButton(self.groupBox_3)
        self.pushButton_select_path.setObjectName(u"pushButton_select_path")

        self.gridLayout_4.addWidget(self.pushButton_select_path, 0, 4, 1, 1)

        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 3, 0, 1, 1)

        self.pushButton_open_folder = QPushButton(self.groupBox_3)
        self.pushButton_open_folder.setObjectName(u"pushButton_open_folder")

        self.gridLayout_4.addWidget(self.pushButton_open_folder, 3, 4, 1, 1)

        self.checkBox_save_all_settings = QCheckBox(self.groupBox_3)
        self.checkBox_save_all_settings.setObjectName(u"checkBox_save_all_settings")

        self.gridLayout_4.addWidget(self.checkBox_save_all_settings, 0, 6, 1, 1)

        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_4.addWidget(self.label_5, 0, 0, 1, 1)

        self.lineEdit_score_title = QLineEdit(self.groupBox_3)
        self.lineEdit_score_title.setObjectName(u"lineEdit_score_title")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_score_title.sizePolicy().hasHeightForWidth())
        self.lineEdit_score_title.setSizePolicy(sizePolicy)

        self.gridLayout_4.addWidget(self.lineEdit_score_title, 3, 1, 1, 1)

        self.comboBox_save_format = QComboBox(self.groupBox_3)
        self.comboBox_save_format.addItem("")
        self.comboBox_save_format.addItem("")
        self.comboBox_save_format.setObjectName(u"comboBox_save_format")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBox_save_format.sizePolicy().hasHeightForWidth())
        self.comboBox_save_format.setSizePolicy(sizePolicy1)
        self.comboBox_save_format.setMinimumSize(QSize(55, 0))

        self.gridLayout_4.addWidget(self.comboBox_save_format, 3, 6, 1, 1)

        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_4.addWidget(self.label_6, 3, 5, 1, 1)

        self.pushButton_rename_folder = QPushButton(self.groupBox_3)
        self.pushButton_rename_folder.setObjectName(u"pushButton_rename_folder")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton_rename_folder.sizePolicy().hasHeightForWidth())
        self.pushButton_rename_folder.setSizePolicy(sizePolicy2)

        self.gridLayout_4.addWidget(self.pushButton_rename_folder, 3, 2, 1, 1)

        self.lineEdit_save_path = QLineEdit(self.groupBox_3)
        self.lineEdit_save_path.setObjectName(u"lineEdit_save_path")

        self.gridLayout_4.addWidget(self.lineEdit_save_path, 0, 1, 1, 3)

        self.checkBox_always_on_top = QCheckBox(self.groupBox_3)
        self.checkBox_always_on_top.setObjectName(u"checkBox_always_on_top")

        self.gridLayout_4.addWidget(self.checkBox_always_on_top, 0, 5, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_3, 0, 0, 1, 3)

        self.groupBox_4 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_5 = QGridLayout(self.groupBox_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.pushButton_clear_capture_data = QPushButton(self.groupBox_4)
        self.pushButton_clear_capture_data.setObjectName(u"pushButton_clear_capture_data")
        sizePolicy1.setHeightForWidth(self.pushButton_clear_capture_data.sizePolicy().hasHeightForWidth())
        self.pushButton_clear_capture_data.setSizePolicy(sizePolicy1)

        self.gridLayout_5.addWidget(self.pushButton_clear_capture_data, 1, 0, 1, 1)

        self.pushButton_clear_score_detections = QPushButton(self.groupBox_4)
        self.pushButton_clear_score_detections.setObjectName(u"pushButton_clear_score_detections")
        sizePolicy1.setHeightForWidth(self.pushButton_clear_score_detections.sizePolicy().hasHeightForWidth())
        self.pushButton_clear_score_detections.setSizePolicy(sizePolicy1)

        self.gridLayout_5.addWidget(self.pushButton_clear_score_detections, 2, 0, 1, 1)

        self.checkBox_imageViewer_show_tools = QCheckBox(self.groupBox_4)
        self.checkBox_imageViewer_show_tools.setObjectName(u"checkBox_imageViewer_show_tools")

        self.gridLayout_5.addWidget(self.checkBox_imageViewer_show_tools, 1, 1, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_4, 11, 1, 1, 2)

        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.doubleSpinBox_opacity = QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_opacity.setObjectName(u"doubleSpinBox_opacity")
        self.doubleSpinBox_opacity.setMinimum(0.100000000000000)
        self.doubleSpinBox_opacity.setMaximum(1.000000000000000)
        self.doubleSpinBox_opacity.setSingleStep(0.010000000000000)
        self.doubleSpinBox_opacity.setValue(0.700000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_opacity, 1, 1, 1, 1)

        self.spinBox_region_height = QSpinBox(self.groupBox)
        self.spinBox_region_height.setObjectName(u"spinBox_region_height")
        sizePolicy2.setHeightForWidth(self.spinBox_region_height.sizePolicy().hasHeightForWidth())
        self.spinBox_region_height.setSizePolicy(sizePolicy2)
        self.spinBox_region_height.setMinimumSize(QSize(80, 0))
        self.spinBox_region_height.setMaximum(2000)

        self.gridLayout.addWidget(self.spinBox_region_height, 2, 7, 1, 1)

        self.line_4 = QFrame(self.groupBox)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_4, 1, 2, 2, 1)

        self.spinBox_region_width = QSpinBox(self.groupBox)
        self.spinBox_region_width.setObjectName(u"spinBox_region_width")
        sizePolicy2.setHeightForWidth(self.spinBox_region_width.sizePolicy().hasHeightForWidth())
        self.spinBox_region_width.setSizePolicy(sizePolicy2)
        self.spinBox_region_width.setMinimumSize(QSize(80, 0))
        self.spinBox_region_width.setMaximum(2000)

        self.gridLayout.addWidget(self.spinBox_region_width, 2, 5, 1, 1)

        self.spinBox_region_y = QSpinBox(self.groupBox)
        self.spinBox_region_y.setObjectName(u"spinBox_region_y")
        sizePolicy2.setHeightForWidth(self.spinBox_region_y.sizePolicy().hasHeightForWidth())
        self.spinBox_region_y.setSizePolicy(sizePolicy2)
        self.spinBox_region_y.setMinimumSize(QSize(80, 0))
        self.spinBox_region_y.setMaximum(2000)

        self.gridLayout.addWidget(self.spinBox_region_y, 1, 7, 1, 1)

        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_11, 1, 6, 1, 1)

        self.checkBox_limit_move = QCheckBox(self.groupBox)
        self.checkBox_limit_move.setObjectName(u"checkBox_limit_move")

        self.gridLayout.addWidget(self.checkBox_limit_move, 2, 1, 1, 1)

        self.spinBox_region_x = QSpinBox(self.groupBox)
        self.spinBox_region_x.setObjectName(u"spinBox_region_x")
        sizePolicy2.setHeightForWidth(self.spinBox_region_x.sizePolicy().hasHeightForWidth())
        self.spinBox_region_x.setSizePolicy(sizePolicy2)
        self.spinBox_region_x.setMinimumSize(QSize(80, 0))
        self.spinBox_region_x.setMaximum(2000)

        self.gridLayout.addWidget(self.spinBox_region_x, 1, 5, 1, 1)

        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_7, 2, 4, 1, 1)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_8, 2, 6, 1, 1)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_9, 1, 4, 1, 1)

        self.checkBox_auto_close = QCheckBox(self.groupBox)
        self.checkBox_auto_close.setObjectName(u"checkBox_auto_close")

        self.gridLayout.addWidget(self.checkBox_auto_close, 2, 0, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox, 11, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy3)
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.comboBox_compare_method = QComboBox(self.groupBox_2)
        self.comboBox_compare_method.addItem("")
        self.comboBox_compare_method.addItem("")
        self.comboBox_compare_method.setObjectName(u"comboBox_compare_method")
        sizePolicy.setHeightForWidth(self.comboBox_compare_method.sizePolicy().hasHeightForWidth())
        self.comboBox_compare_method.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.comboBox_compare_method, 2, 2, 1, 1)

        self.label_14 = QLabel(self.groupBox_2)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_14, 1, 0, 1, 1)

        self.doubleSpinBox_compare_threshold = QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_compare_threshold.setObjectName(u"doubleSpinBox_compare_threshold")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_compare_threshold.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_compare_threshold.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_compare_threshold.setMaximum(65535.000000000000000)
        self.doubleSpinBox_compare_threshold.setSingleStep(0.100000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_compare_threshold, 1, 5, 1, 1)

        self.pushButton_image_rebuild = QPushButton(self.groupBox_2)
        self.pushButton_image_rebuild.setObjectName(u"pushButton_image_rebuild")
        self.pushButton_image_rebuild.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButton_image_rebuild, 1, 9, 1, 1)

        self.pushButton_image_reorder = QPushButton(self.groupBox_2)
        self.pushButton_image_reorder.setObjectName(u"pushButton_image_reorder")
        sizePolicy2.setHeightForWidth(self.pushButton_image_reorder.sizePolicy().hasHeightForWidth())
        self.pushButton_image_reorder.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.pushButton_image_reorder, 2, 9, 1, 1)

        self.comboBox_capture_tool = QComboBox(self.groupBox_2)
        self.comboBox_capture_tool.addItem("")
        self.comboBox_capture_tool.addItem("")
        self.comboBox_capture_tool.addItem("")
        self.comboBox_capture_tool.setObjectName(u"comboBox_capture_tool")
        sizePolicy.setHeightForWidth(self.comboBox_capture_tool.sizePolicy().hasHeightForWidth())
        self.comboBox_capture_tool.setSizePolicy(sizePolicy)
        self.comboBox_capture_tool.setMinimumSize(QSize(90, 0))

        self.gridLayout_2.addWidget(self.comboBox_capture_tool, 1, 2, 1, 1)

        self.doubleSpinBox_capture_delay = QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_capture_delay.setObjectName(u"doubleSpinBox_capture_delay")
        self.doubleSpinBox_capture_delay.setMinimum(0.100000000000000)
        self.doubleSpinBox_capture_delay.setSingleStep(0.100000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_capture_delay, 2, 5, 1, 1)

        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_2.addWidget(self.label_13, 2, 4, 1, 1)

        self.checkBox_reverse_image = QCheckBox(self.groupBox_2)
        self.checkBox_reverse_image.setObjectName(u"checkBox_reverse_image")

        self.gridLayout_2.addWidget(self.checkBox_reverse_image, 2, 7, 1, 1)

        self.checkBox_keep_last = QCheckBox(self.groupBox_2)
        self.checkBox_keep_last.setObjectName(u"checkBox_keep_last")

        self.gridLayout_2.addWidget(self.checkBox_keep_last, 1, 7, 1, 1)

        self.label_20 = QLabel(self.groupBox_2)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_20, 2, 0, 1, 1)

        self.label_16 = QLabel(self.groupBox_2)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_2.addWidget(self.label_16, 1, 4, 1, 1)

        self.line = QFrame(self.groupBox_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line, 1, 3, 2, 1)

        self.line_8 = QFrame(self.groupBox_2)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.Shape.VLine)
        self.line_8.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line_8, 1, 8, 2, 1)

        self.line_3 = QFrame(self.groupBox_2)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line_3, 1, 6, 2, 1)


        self.gridLayout_3.addWidget(self.groupBox_2, 1, 0, 1, 3)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(TabSettings)

        QMetaObject.connectSlotsByName(TabSettings)
    # setupUi

    def retranslateUi(self, TabSettings):
        TabSettings.setWindowTitle(QCoreApplication.translate("TabSettings", u"Form", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("TabSettings", u"\u5168\u5c40\u8bbe\u7f6e", None))
        self.pushButton_select_folder.setText(QCoreApplication.translate("TabSettings", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.pushButton_select_path.setText(QCoreApplication.translate("TabSettings", u"\u6d4f\u89c8\u76ee\u5f55", None))
        self.label_3.setText(QCoreApplication.translate("TabSettings", u"\u66f2\u8c31\u6807\u9898\uff1a", None))
        self.pushButton_open_folder.setText(QCoreApplication.translate("TabSettings", u"\u6253\u5f00\u76ee\u5f55", None))
        self.checkBox_save_all_settings.setText(QCoreApplication.translate("TabSettings", u"\u4fdd\u5b58\u6240\u6709\u8bbe\u7f6e", None))
        self.label_5.setText(QCoreApplication.translate("TabSettings", u"\u5b58\u50a8\u8def\u5f84\uff1a", None))
        self.comboBox_save_format.setItemText(0, QCoreApplication.translate("TabSettings", u".jpg", None))
        self.comboBox_save_format.setItemText(1, QCoreApplication.translate("TabSettings", u".png", None))

        self.label_6.setText(QCoreApplication.translate("TabSettings", u"\u5b58\u50a8\u683c\u5f0f\uff1a", None))
        self.pushButton_rename_folder.setText(QCoreApplication.translate("TabSettings", u"\u91cd\u547d\u540d", None))
        self.checkBox_always_on_top.setText(QCoreApplication.translate("TabSettings", u"\u7a97\u53e3\u7f6e\u9876", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("TabSettings", u"\u5176\u4ed6", None))
#if QT_CONFIG(tooltip)
        self.pushButton_clear_capture_data.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>Cached diff between captures, used to build images from captures.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_clear_capture_data.setText(QCoreApplication.translate("TabSettings", u"\u6e05\u9664CaptureData", None))
#if QT_CONFIG(tooltip)
        self.pushButton_clear_score_detections.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>Cached diff between captures, used to build images from captures.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_clear_score_detections.setText(QCoreApplication.translate("TabSettings", u"\u6e05\u9664ScoreDetections", None))
        self.checkBox_imageViewer_show_tools.setText(QCoreApplication.translate("TabSettings", u"\u663e\u793a\u9884\u89c8\u5de5\u5177", None))
        self.groupBox.setTitle(QCoreApplication.translate("TabSettings", u"\u5b9a\u4f4d\u8bbe\u7f6e", None))
        self.label_11.setText(QCoreApplication.translate("TabSettings", u"Y:", None))
        self.checkBox_limit_move.setText(QCoreApplication.translate("TabSettings", u"\u9650\u5236\u79fb\u52a8\u8303\u56f4", None))
        self.label_10.setText(QCoreApplication.translate("TabSettings", u"\u7a97\u53e3\u900f\u660e\u5ea6:", None))
        self.label_7.setText(QCoreApplication.translate("TabSettings", u"\u5bbd:", None))
        self.label_8.setText(QCoreApplication.translate("TabSettings", u"\u9ad8:", None))
        self.label_9.setText(QCoreApplication.translate("TabSettings", u"X:", None))
        self.checkBox_auto_close.setText(QCoreApplication.translate("TabSettings", u"\u81ea\u52a8\u5173\u95ed\u7a97\u53e3", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("TabSettings", u"\u622a\u56fe\u8bbe\u7f6e", None))
        self.comboBox_compare_method.setItemText(0, QCoreApplication.translate("TabSettings", u"SSIM", None))
        self.comboBox_compare_method.setItemText(1, QCoreApplication.translate("TabSettings", u"MSE", None))

        self.label_14.setText(QCoreApplication.translate("TabSettings", u"\u6bd4\u8f83\u7b97\u6cd5\uff1a", None))
        self.pushButton_image_rebuild.setText(QCoreApplication.translate("TabSettings", u"\u91cd\u6784\u5efaimage", None))
        self.pushButton_image_reorder.setText(QCoreApplication.translate("TabSettings", u"\u91cd\u7f16\u53f7image", None))
        self.comboBox_capture_tool.setItemText(0, QCoreApplication.translate("TabSettings", u"mss", None))
        self.comboBox_capture_tool.setItemText(1, QCoreApplication.translate("TabSettings", u"spectacle", None))
        self.comboBox_capture_tool.setItemText(2, QCoreApplication.translate("TabSettings", u"grim", None))

        self.label_13.setText(QCoreApplication.translate("TabSettings", u"\u622a\u56fe\u95f4\u9694(\u79d2/s)\uff1a", None))
        self.checkBox_reverse_image.setText(QCoreApplication.translate("TabSettings", u"\u5bf9\u56fe\u7247\u8fdb\u884c\u53cd\u76f8", None))
        self.checkBox_keep_last.setText(QCoreApplication.translate("TabSettings", u"\u4fdd\u7559\u6700\u540e\u4e00\u7ec4\u622a\u56fe", None))
        self.label_20.setText(QCoreApplication.translate("TabSettings", u"\u622a\u56fe\u5de5\u5177\uff1a", None))
        self.label_16.setText(QCoreApplication.translate("TabSettings", u"\u622a\u81f3\u5dee\u5f02\u503c\uff1a", None))
    # retranslateUi

