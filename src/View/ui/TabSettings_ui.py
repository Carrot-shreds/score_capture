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
        TabSettings.resize(1001, 568)
        self.verticalLayout = QVBoxLayout(TabSettings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(TabSettings)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 981, 548))
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
        self.checkBox_imageViewer_show_tools = QCheckBox(self.groupBox_4)
        self.checkBox_imageViewer_show_tools.setObjectName(u"checkBox_imageViewer_show_tools")

        self.gridLayout_5.addWidget(self.checkBox_imageViewer_show_tools, 1, 1, 1, 1)

        self.pushButton_clear_score_detections = QPushButton(self.groupBox_4)
        self.pushButton_clear_score_detections.setObjectName(u"pushButton_clear_score_detections")
        sizePolicy2.setHeightForWidth(self.pushButton_clear_score_detections.sizePolicy().hasHeightForWidth())
        self.pushButton_clear_score_detections.setSizePolicy(sizePolicy2)

        self.gridLayout_5.addWidget(self.pushButton_clear_score_detections, 2, 0, 1, 1)

        self.pushButton_clear_capture_data = QPushButton(self.groupBox_4)
        self.pushButton_clear_capture_data.setObjectName(u"pushButton_clear_capture_data")
        sizePolicy2.setHeightForWidth(self.pushButton_clear_capture_data.sizePolicy().hasHeightForWidth())
        self.pushButton_clear_capture_data.setSizePolicy(sizePolicy2)

        self.gridLayout_5.addWidget(self.pushButton_clear_capture_data, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_4, 11, 1, 1, 2)

        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy3)
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.comboBox_capture_tool = QComboBox(self.groupBox_2)
        self.comboBox_capture_tool.addItem("")
        self.comboBox_capture_tool.addItem("")
        self.comboBox_capture_tool.addItem("")
        self.comboBox_capture_tool.setObjectName(u"comboBox_capture_tool")
        sizePolicy.setHeightForWidth(self.comboBox_capture_tool.sizePolicy().hasHeightForWidth())
        self.comboBox_capture_tool.setSizePolicy(sizePolicy)
        self.comboBox_capture_tool.setMinimumSize(QSize(90, 0))

        self.gridLayout_2.addWidget(self.comboBox_capture_tool, 1, 2, 1, 1)

        self.label_14 = QLabel(self.groupBox_2)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_14, 1, 0, 1, 1)

        self.line_8 = QFrame(self.groupBox_2)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.Shape.VLine)
        self.line_8.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line_8, 1, 8, 2, 1)

        self.doubleSpinBox_capture_delay = QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_capture_delay.setObjectName(u"doubleSpinBox_capture_delay")
        self.doubleSpinBox_capture_delay.setMinimum(0.100000000000000)
        self.doubleSpinBox_capture_delay.setSingleStep(0.100000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_capture_delay, 2, 5, 1, 1)

        self.pushButton_image_reorder = QPushButton(self.groupBox_2)
        self.pushButton_image_reorder.setObjectName(u"pushButton_image_reorder")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pushButton_image_reorder.sizePolicy().hasHeightForWidth())
        self.pushButton_image_reorder.setSizePolicy(sizePolicy4)

        self.gridLayout_2.addWidget(self.pushButton_image_reorder, 2, 9, 1, 1)

        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_2.addWidget(self.label_13, 2, 4, 1, 1)

        self.line = QFrame(self.groupBox_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line, 1, 3, 2, 1)

        self.doubleSpinBox_compare_threshold = QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_compare_threshold.setObjectName(u"doubleSpinBox_compare_threshold")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_compare_threshold.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_compare_threshold.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_compare_threshold.setMaximum(65535.000000000000000)
        self.doubleSpinBox_compare_threshold.setSingleStep(0.100000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_compare_threshold, 1, 5, 1, 1)

        self.checkBox_invert_image = QCheckBox(self.groupBox_2)
        self.checkBox_invert_image.setObjectName(u"checkBox_invert_image")

        self.gridLayout_2.addWidget(self.checkBox_invert_image, 2, 7, 1, 1)

        self.label_16 = QLabel(self.groupBox_2)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_2.addWidget(self.label_16, 1, 4, 1, 1)

        self.checkBox_keep_last = QCheckBox(self.groupBox_2)
        self.checkBox_keep_last.setObjectName(u"checkBox_keep_last")

        self.gridLayout_2.addWidget(self.checkBox_keep_last, 1, 7, 1, 1)

        self.pushButton_image_rebuild = QPushButton(self.groupBox_2)
        self.pushButton_image_rebuild.setObjectName(u"pushButton_image_rebuild")
        sizePolicy4.setHeightForWidth(self.pushButton_image_rebuild.sizePolicy().hasHeightForWidth())
        self.pushButton_image_rebuild.setSizePolicy(sizePolicy4)
        self.pushButton_image_rebuild.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButton_image_rebuild, 1, 9, 1, 1)

        self.line_3 = QFrame(self.groupBox_2)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line_3, 1, 6, 2, 1)

        self.comboBox_compare_method = QComboBox(self.groupBox_2)
        self.comboBox_compare_method.addItem("")
        self.comboBox_compare_method.addItem("")
        self.comboBox_compare_method.setObjectName(u"comboBox_compare_method")
        sizePolicy.setHeightForWidth(self.comboBox_compare_method.sizePolicy().hasHeightForWidth())
        self.comboBox_compare_method.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.comboBox_compare_method, 2, 2, 1, 1)

        self.label_20 = QLabel(self.groupBox_2)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_20, 2, 0, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_2, 1, 0, 1, 3)

        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)

        self.spinBox_region_height = QSpinBox(self.groupBox)
        self.spinBox_region_height.setObjectName(u"spinBox_region_height")
        sizePolicy2.setHeightForWidth(self.spinBox_region_height.sizePolicy().hasHeightForWidth())
        self.spinBox_region_height.setSizePolicy(sizePolicy2)
        self.spinBox_region_height.setMinimumSize(QSize(80, 0))
        self.spinBox_region_height.setMaximum(2000)

        self.gridLayout.addWidget(self.spinBox_region_height, 2, 8, 1, 1)

        self.line_4 = QFrame(self.groupBox)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_4, 1, 2, 2, 1)

        self.checkBox_auto_close = QCheckBox(self.groupBox)
        self.checkBox_auto_close.setObjectName(u"checkBox_auto_close")

        self.gridLayout.addWidget(self.checkBox_auto_close, 2, 0, 1, 1)

        self.spinBox_region_x = QSpinBox(self.groupBox)
        self.spinBox_region_x.setObjectName(u"spinBox_region_x")
        sizePolicy2.setHeightForWidth(self.spinBox_region_x.sizePolicy().hasHeightForWidth())
        self.spinBox_region_x.setSizePolicy(sizePolicy2)
        self.spinBox_region_x.setMinimumSize(QSize(80, 0))
        self.spinBox_region_x.setMaximum(2000)

        self.gridLayout.addWidget(self.spinBox_region_x, 1, 5, 1, 1)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_9, 1, 4, 1, 1)

        self.checkBox_limit_move = QCheckBox(self.groupBox)
        self.checkBox_limit_move.setObjectName(u"checkBox_limit_move")

        self.gridLayout.addWidget(self.checkBox_limit_move, 2, 1, 1, 1)

        self.doubleSpinBox_opacity = QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_opacity.setObjectName(u"doubleSpinBox_opacity")
        self.doubleSpinBox_opacity.setMinimum(0.100000000000000)
        self.doubleSpinBox_opacity.setMaximum(1.000000000000000)
        self.doubleSpinBox_opacity.setSingleStep(0.010000000000000)
        self.doubleSpinBox_opacity.setValue(0.700000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_opacity, 1, 1, 1, 1)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_7, 1, 7, 1, 1)

        self.spinBox_region_width = QSpinBox(self.groupBox)
        self.spinBox_region_width.setObjectName(u"spinBox_region_width")
        sizePolicy2.setHeightForWidth(self.spinBox_region_width.sizePolicy().hasHeightForWidth())
        self.spinBox_region_width.setSizePolicy(sizePolicy2)
        self.spinBox_region_width.setMinimumSize(QSize(80, 0))
        self.spinBox_region_width.setMaximum(2000)

        self.gridLayout.addWidget(self.spinBox_region_width, 1, 8, 1, 1)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_8, 2, 7, 1, 1)

        self.spinBox_region_y = QSpinBox(self.groupBox)
        self.spinBox_region_y.setObjectName(u"spinBox_region_y")
        sizePolicy2.setHeightForWidth(self.spinBox_region_y.sizePolicy().hasHeightForWidth())
        self.spinBox_region_y.setSizePolicy(sizePolicy2)
        self.spinBox_region_y.setMinimumSize(QSize(80, 0))
        self.spinBox_region_y.setMaximum(2000)

        self.gridLayout.addWidget(self.spinBox_region_y, 2, 5, 1, 1)

        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_11, 2, 4, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox, 11, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(TabSettings)

        QMetaObject.connectSlotsByName(TabSettings)
    # setupUi

    def retranslateUi(self, TabSettings):
        TabSettings.setWindowTitle(QCoreApplication.translate("TabSettings", u"Form", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("TabSettings", u"Global", None))
#if QT_CONFIG(tooltip)
        self.pushButton_select_folder.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>Open a folder as working dir.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_select_folder.setText(QCoreApplication.translate("TabSettings", u"Open", None))
#if QT_CONFIG(tooltip)
        self.pushButton_select_path.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>Browse and open a folder as the main out directory.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_select_path.setText(QCoreApplication.translate("TabSettings", u"Browse", None))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>Also as title of images and the score.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("TabSettings", u"Folder Title:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_open_folder.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>Reveal working dir in file explorer.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_open_folder.setText(QCoreApplication.translate("TabSettings", u"Reveal", None))
#if QT_CONFIG(tooltip)
        self.checkBox_save_all_settings.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>Saving ALL settings when closed. If not, will only save settings which be setted to true in AppSettingsSavingConfig.json.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_save_all_settings.setText(QCoreApplication.translate("TabSettings", u"Save All Settings", None))
        self.label_5.setText(QCoreApplication.translate("TabSettings", u"Main Output Dir:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_score_title.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>Also used as title of files and score.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_save_format.setItemText(0, QCoreApplication.translate("TabSettings", u".jpg", None))
        self.comboBox_save_format.setItemText(1, QCoreApplication.translate("TabSettings", u".png", None))

        self.label_6.setText(QCoreApplication.translate("TabSettings", u"Saving Format:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_rename_folder.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>Rename the folder and all image names including title.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_rename_folder.setText(QCoreApplication.translate("TabSettings", u"Rename", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_save_path.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>Working dir = main_out_dir // folder_title</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_always_on_top.setText(QCoreApplication.translate("TabSettings", u"Always on Top", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("TabSettings", u"Others", None))
        self.checkBox_imageViewer_show_tools.setText(QCoreApplication.translate("TabSettings", u"Show ImageViewer tools", None))
#if QT_CONFIG(tooltip)
        self.pushButton_clear_score_detections.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>Cached detected lines data, used to stitch images as reference.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_clear_score_detections.setText(QCoreApplication.translate("TabSettings", u"Clear ScoreDetections", None))
#if QT_CONFIG(tooltip)
        self.pushButton_clear_capture_data.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>Cached diff between captures, used to build images from captures.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_clear_capture_data.setText(QCoreApplication.translate("TabSettings", u"Clear CaptureData", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("TabSettings", u"Capture", None))
        self.comboBox_capture_tool.setItemText(0, QCoreApplication.translate("TabSettings", u"mss", None))
        self.comboBox_capture_tool.setItemText(1, QCoreApplication.translate("TabSettings", u"spectacle", None))
        self.comboBox_capture_tool.setItemText(2, QCoreApplication.translate("TabSettings", u"grim", None))

#if QT_CONFIG(tooltip)
        self.comboBox_capture_tool.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>MSS: cross-platform, supports multiple screens. But doesn't work on Wayland.</p><p>Spectacle: KDE default CLI capture tool.</p><p>Grim: Alternative wayland capture tool.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_14.setText(QCoreApplication.translate("TabSettings", u"Capture Tool:", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_capture_delay.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>Capture inverval (Seconds)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.doubleSpinBox_capture_delay.setSpecialValueText("")
#if QT_CONFIG(tooltip)
        self.pushButton_image_reorder.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>Reorder and rename image filenames.</p><p>This is needed when you doesn't want some image and deleted them.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_image_reorder.setText(QCoreApplication.translate("TabSettings", u"Reorder Image", None))
        self.label_13.setText(QCoreApplication.translate("TabSettings", u"Interval (s):", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_compare_threshold.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>When compare result of previous two captures exceeds the threshold. We think that the screen switch to a new different image, then we build a new image from these captures by average them.</p><p>SSIM: 0-1 (usually in 0.93-0.97)</p><p>MSE: 0-65535</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.checkBox_invert_image.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p><span style=\" font-family:'quote-cjk-patch','Inter','system-ui','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Open Sans','Helvetica Neue','sans-serif'; font-size:16px; color:#0f1115; background-color:#ffffff;\">Converts image to its complementary colors.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_invert_image.setText(QCoreApplication.translate("TabSettings", u"Invert Images", None))
        self.label_16.setText(QCoreApplication.translate("TabSettings", u"Threshold:", None))
#if QT_CONFIG(tooltip)
        self.checkBox_keep_last.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>Whether keep the last group capture as a image when capture stopped.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_keep_last.setText(QCoreApplication.translate("TabSettings", u"Keep Last group", None))
#if QT_CONFIG(tooltip)
        self.pushButton_image_rebuild.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>Compare captures and rebuild images using current settings.</p><p>This can be used to manually clean some captures to get better image.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_image_rebuild.setText(QCoreApplication.translate("TabSettings", u"Rebuild Image", None))
        self.comboBox_compare_method.setItemText(0, QCoreApplication.translate("TabSettings", u"SSIM", None))
        self.comboBox_compare_method.setItemText(1, QCoreApplication.translate("TabSettings", u"MSE", None))

#if QT_CONFIG(tooltip)
        self.comboBox_compare_method.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>SSIM: A bit slower but have way better result. Recommended.</p><p>MSE: Less cpu usage.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_20.setText(QCoreApplication.translate("TabSettings", u"Compare Method:", None))
        self.groupBox.setTitle(QCoreApplication.translate("TabSettings", u"Locate", None))
        self.label_10.setText(QCoreApplication.translate("TabSettings", u"Window Opacity:", None))
#if QT_CONFIG(tooltip)
        self.checkBox_auto_close.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>Auto close when click locate button and updated region.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_auto_close.setText(QCoreApplication.translate("TabSettings", u"Auto Close", None))
        self.label_9.setText(QCoreApplication.translate("TabSettings", u"X:", None))
#if QT_CONFIG(tooltip)
        self.checkBox_limit_move.setToolTip(QCoreApplication.translate("TabSettings", u"<html><head/><body><p>Limit the window movement, make it can not out of the screen.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_limit_move.setText(QCoreApplication.translate("TabSettings", u"Limit on Screen", None))
        self.label_7.setText(QCoreApplication.translate("TabSettings", u"Width:", None))
        self.label_8.setText(QCoreApplication.translate("TabSettings", u"Height:", None))
        self.label_11.setText(QCoreApplication.translate("TabSettings", u"Y:", None))
    # retranslateUi

