# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TabPreview.ui'
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
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpinBox,
    QSplitter, QVBoxLayout, QWidget)

from ..widgets.ImageViewer import ImageViewer

class Ui_TabPreview(object):
    def setupUi(self, TabPreview):
        if not TabPreview.objectName():
            TabPreview.setObjectName(u"TabPreview")
        TabPreview.resize(1103, 281)
        self.verticalLayout = QVBoxLayout(TabPreview)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(TabPreview)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.setHandleWidth(10)
        self.splitter.setChildrenCollapsible(False)
        self.gridFrame = QFrame(self.splitter)
        self.gridFrame.setObjectName(u"gridFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gridFrame.sizePolicy().hasHeightForWidth())
        self.gridFrame.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.gridFrame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox_detect_coefficients = QGroupBox(self.gridFrame)
        self.groupBox_detect_coefficients.setObjectName(u"groupBox_detect_coefficients")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_detect_coefficients.sizePolicy().hasHeightForWidth())
        self.groupBox_detect_coefficients.setSizePolicy(sizePolicy1)
        self.groupBox_detect_coefficients.setFlat(False)
        self.gridLayout = QGridLayout(self.groupBox_detect_coefficients)
        self.gridLayout.setObjectName(u"gridLayout")
        self.doubleSpinBox_detect_coefficient_vertical = QDoubleSpinBox(self.groupBox_detect_coefficients)
        self.doubleSpinBox_detect_coefficient_vertical.setObjectName(u"doubleSpinBox_detect_coefficient_vertical")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_detect_coefficient_vertical.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_detect_coefficient_vertical.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_detect_coefficient_vertical.setDecimals(3)
        self.doubleSpinBox_detect_coefficient_vertical.setMinimum(0.001000000000000)
        self.doubleSpinBox_detect_coefficient_vertical.setMaximum(1.000000000000000)
        self.doubleSpinBox_detect_coefficient_vertical.setSingleStep(0.010000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_detect_coefficient_vertical, 1, 1, 1, 1)

        self.doubleSpinBox_detect_coefficient_horizontal = QDoubleSpinBox(self.groupBox_detect_coefficients)
        self.doubleSpinBox_detect_coefficient_horizontal.setObjectName(u"doubleSpinBox_detect_coefficient_horizontal")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_detect_coefficient_horizontal.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_detect_coefficient_horizontal.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_detect_coefficient_horizontal.setDecimals(3)
        self.doubleSpinBox_detect_coefficient_horizontal.setMinimum(0.001000000000000)
        self.doubleSpinBox_detect_coefficient_horizontal.setMaximum(1.000000000000000)
        self.doubleSpinBox_detect_coefficient_horizontal.setSingleStep(0.010000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_detect_coefficient_horizontal, 0, 1, 1, 1)

        self.label_detect_coefficient_vertical = QLabel(self.groupBox_detect_coefficients)
        self.label_detect_coefficient_vertical.setObjectName(u"label_detect_coefficient_vertical")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_detect_coefficient_vertical.sizePolicy().hasHeightForWidth())
        self.label_detect_coefficient_vertical.setSizePolicy(sizePolicy3)
        self.label_detect_coefficient_vertical.setMinimumSize(QSize(0, 0))
        self.label_detect_coefficient_vertical.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_detect_coefficient_vertical, 1, 0, 1, 1)

        self.label_detect_coefficient_horizontal = QLabel(self.groupBox_detect_coefficients)
        self.label_detect_coefficient_horizontal.setObjectName(u"label_detect_coefficient_horizontal")
        sizePolicy3.setHeightForWidth(self.label_detect_coefficient_horizontal.sizePolicy().hasHeightForWidth())
        self.label_detect_coefficient_horizontal.setSizePolicy(sizePolicy3)
        self.label_detect_coefficient_horizontal.setMinimumSize(QSize(0, 0))
        self.label_detect_coefficient_horizontal.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_detect_coefficient_horizontal, 0, 0, 1, 1)


        self.horizontalLayout_2.addWidget(self.groupBox_detect_coefficients)

        self.groupBox_3 = QGroupBox(self.gridFrame)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_4 = QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.doubleSpinBox_h_invert_pixel_threshold = QDoubleSpinBox(self.groupBox_3)
        self.doubleSpinBox_h_invert_pixel_threshold.setObjectName(u"doubleSpinBox_h_invert_pixel_threshold")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_h_invert_pixel_threshold.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_h_invert_pixel_threshold.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_h_invert_pixel_threshold.setDecimals(2)
        self.doubleSpinBox_h_invert_pixel_threshold.setMinimum(1.000000000000000)
        self.doubleSpinBox_h_invert_pixel_threshold.setMaximum(255.000000000000000)
        self.doubleSpinBox_h_invert_pixel_threshold.setSingleStep(0.100000000000000)

        self.gridLayout_4.addWidget(self.doubleSpinBox_h_invert_pixel_threshold, 0, 1, 1, 1)

        self.label_detect_coefficient_horizontal_3 = QLabel(self.groupBox_3)
        self.label_detect_coefficient_horizontal_3.setObjectName(u"label_detect_coefficient_horizontal_3")
        sizePolicy3.setHeightForWidth(self.label_detect_coefficient_horizontal_3.sizePolicy().hasHeightForWidth())
        self.label_detect_coefficient_horizontal_3.setSizePolicy(sizePolicy3)
        self.label_detect_coefficient_horizontal_3.setMinimumSize(QSize(0, 0))
        self.label_detect_coefficient_horizontal_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_detect_coefficient_horizontal_3, 2, 0, 1, 1)

        self.label_detect_coefficient_horizontal_2 = QLabel(self.groupBox_3)
        self.label_detect_coefficient_horizontal_2.setObjectName(u"label_detect_coefficient_horizontal_2")
        sizePolicy3.setHeightForWidth(self.label_detect_coefficient_horizontal_2.sizePolicy().hasHeightForWidth())
        self.label_detect_coefficient_horizontal_2.setSizePolicy(sizePolicy3)
        self.label_detect_coefficient_horizontal_2.setMinimumSize(QSize(0, 0))
        self.label_detect_coefficient_horizontal_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_detect_coefficient_horizontal_2, 0, 0, 1, 1)

        self.spinBox_h_invert_thickness_threshold = QSpinBox(self.groupBox_3)
        self.spinBox_h_invert_thickness_threshold.setObjectName(u"spinBox_h_invert_thickness_threshold")
        self.spinBox_h_invert_thickness_threshold.setMinimum(1)
        self.spinBox_h_invert_thickness_threshold.setMaximum(500)

        self.gridLayout_4.addWidget(self.spinBox_h_invert_thickness_threshold, 2, 1, 1, 1)


        self.horizontalLayout_2.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.gridFrame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy3.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy3)
        self.groupBox_2.setFlat(False)
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.checkBox_invert_horizontal = QCheckBox(self.groupBox_2)
        self.checkBox_invert_horizontal.setObjectName(u"checkBox_invert_horizontal")

        self.gridLayout_2.addWidget(self.checkBox_invert_horizontal, 1, 0, 1, 1)

        self.pushButton_detect_lines = QPushButton(self.groupBox_2)
        self.pushButton_detect_lines.setObjectName(u"pushButton_detect_lines")
        sizePolicy2.setHeightForWidth(self.pushButton_detect_lines.sizePolicy().hasHeightForWidth())
        self.pushButton_detect_lines.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.pushButton_detect_lines, 0, 2, 1, 1)

        self.pushButton_clear_lines = QPushButton(self.groupBox_2)
        self.pushButton_clear_lines.setObjectName(u"pushButton_clear_lines")
        sizePolicy2.setHeightForWidth(self.pushButton_clear_lines.sizePolicy().hasHeightForWidth())
        self.pushButton_clear_lines.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.pushButton_clear_lines, 1, 2, 1, 1)

        self.checkBox_live_detect = QCheckBox(self.groupBox_2)
        self.checkBox_live_detect.setObjectName(u"checkBox_live_detect")
        sizePolicy2.setHeightForWidth(self.checkBox_live_detect.sizePolicy().hasHeightForWidth())
        self.checkBox_live_detect.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.checkBox_live_detect, 1, 1, 1, 1)

        self.comboBox_line_type = QComboBox(self.groupBox_2)
        self.comboBox_line_type.addItem("")
        self.comboBox_line_type.addItem("")
        self.comboBox_line_type.addItem("")
        self.comboBox_line_type.setObjectName(u"comboBox_line_type")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.comboBox_line_type.sizePolicy().hasHeightForWidth())
        self.comboBox_line_type.setSizePolicy(sizePolicy4)
        self.comboBox_line_type.setMinimumSize(QSize(100, 0))

        self.gridLayout_2.addWidget(self.comboBox_line_type, 0, 0, 1, 2)


        self.horizontalLayout_2.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.gridFrame)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy3.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy3)
        self.groupBox.setFlat(False)
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.checkBox_live_preview = QCheckBox(self.groupBox)
        self.checkBox_live_preview.setObjectName(u"checkBox_live_preview")
        sizePolicy2.setHeightForWidth(self.checkBox_live_preview.sizePolicy().hasHeightForWidth())
        self.checkBox_live_preview.setSizePolicy(sizePolicy2)

        self.gridLayout_3.addWidget(self.checkBox_live_preview, 1, 1, 1, 1)

        self.pushButton_update_image = QPushButton(self.groupBox)
        self.pushButton_update_image.setObjectName(u"pushButton_update_image")
        sizePolicy2.setHeightForWidth(self.pushButton_update_image.sizePolicy().hasHeightForWidth())
        self.pushButton_update_image.setSizePolicy(sizePolicy2)

        self.gridLayout_3.addWidget(self.pushButton_update_image, 0, 1, 1, 1)

        self.checkBox_save_preview = QCheckBox(self.groupBox)
        self.checkBox_save_preview.setObjectName(u"checkBox_save_preview")
        sizePolicy2.setHeightForWidth(self.checkBox_save_preview.sizePolicy().hasHeightForWidth())
        self.checkBox_save_preview.setSizePolicy(sizePolicy2)

        self.gridLayout_3.addWidget(self.checkBox_save_preview, 1, 2, 1, 1)

        self.pushButton_glob_image = QPushButton(self.groupBox)
        self.pushButton_glob_image.setObjectName(u"pushButton_glob_image")
        sizePolicy2.setHeightForWidth(self.pushButton_glob_image.sizePolicy().hasHeightForWidth())
        self.pushButton_glob_image.setSizePolicy(sizePolicy2)

        self.gridLayout_3.addWidget(self.pushButton_glob_image, 1, 3, 1, 1)

        self.pushButton_invert_image = QPushButton(self.groupBox)
        self.pushButton_invert_image.setObjectName(u"pushButton_invert_image")
        sizePolicy2.setHeightForWidth(self.pushButton_invert_image.sizePolicy().hasHeightForWidth())
        self.pushButton_invert_image.setSizePolicy(sizePolicy2)

        self.gridLayout_3.addWidget(self.pushButton_invert_image, 0, 2, 1, 1)

        self.pushButton_open_image = QPushButton(self.groupBox)
        self.pushButton_open_image.setObjectName(u"pushButton_open_image")
        sizePolicy2.setHeightForWidth(self.pushButton_open_image.sizePolicy().hasHeightForWidth())
        self.pushButton_open_image.setSizePolicy(sizePolicy2)

        self.gridLayout_3.addWidget(self.pushButton_open_image, 0, 3, 1, 1)


        self.horizontalLayout_2.addWidget(self.groupBox)

        self.splitter.addWidget(self.gridFrame)
        self.ImageViewer = ImageViewer(self.splitter)
        self.ImageViewer.setObjectName(u"ImageViewer")
        self.splitter.addWidget(self.ImageViewer)

        self.verticalLayout.addWidget(self.splitter)


        self.retranslateUi(TabPreview)

        QMetaObject.connectSlotsByName(TabPreview)
    # setupUi

    def retranslateUi(self, TabPreview):
        TabPreview.setWindowTitle(QCoreApplication.translate("TabPreview", u"Form", None))
        self.groupBox_detect_coefficients.setTitle(QCoreApplication.translate("TabPreview", u"Line Detection Parameters", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_detect_coefficient_vertical.setToolTip(QCoreApplication.translate("TabPreview", u"<html><head/><body><p>Large number for less vertical lines. Between 0 and 1.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_detect_coefficient_horizontal.setToolTip(QCoreApplication.translate("TabPreview", u"<html><head/><body><p>Large number for less horizontal lines. Between 0 and 1.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_detect_coefficient_vertical.setText(QCoreApplication.translate("TabPreview", u"Vertical:", None))
        self.label_detect_coefficient_horizontal.setText(QCoreApplication.translate("TabPreview", u"Horizontal:", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("TabPreview", u"Invert Horizontal Line Threshold", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_h_invert_pixel_threshold.setToolTip(QCoreApplication.translate("TabPreview", u"<html><head/><body><p>Large number for less gap lines. Between 0 and 255. Usually in 254-255.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_detect_coefficient_horizontal_3.setText(QCoreApplication.translate("TabPreview", u"Min. Thickness:", None))
        self.label_detect_coefficient_horizontal_2.setText(QCoreApplication.translate("TabPreview", u"Pixel Mean:", None))
#if QT_CONFIG(tooltip)
        self.spinBox_h_invert_thickness_threshold.setToolTip(QCoreApplication.translate("TabPreview", u"<html><head/><body><p>The minimum thickness threshold for detection.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_2.setTitle(QCoreApplication.translate("TabPreview", u"Preview Settings", None))
#if QT_CONFIG(tooltip)
        self.checkBox_invert_horizontal.setToolTip(QCoreApplication.translate("TabPreview", u"<html><head/><body><p>Preview inverted horizontal lines instead of normal. These lines will be used to cut reclip images to single pages.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_invert_horizontal.setText(QCoreApplication.translate("TabPreview", u"Invert H. Line", None))
#if QT_CONFIG(tooltip)
        self.pushButton_detect_lines.setToolTip(QCoreApplication.translate("TabPreview", u"<html><head/><body><p>Detect lines and update preview.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_detect_lines.setText(QCoreApplication.translate("TabPreview", u"Detect", None))
#if QT_CONFIG(tooltip)
        self.pushButton_clear_lines.setToolTip(QCoreApplication.translate("TabPreview", u"<html><head/><body><p>Restore image from line detected or inverted.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_clear_lines.setText(QCoreApplication.translate("TabPreview", u"Restore", None))
#if QT_CONFIG(tooltip)
        self.checkBox_live_detect.setToolTip(QCoreApplication.translate("TabPreview", u"<html><head/><body><p>Automatically redetect image when detection parameters changed.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_live_detect.setText(QCoreApplication.translate("TabPreview", u"Live Detect", None))
        self.comboBox_line_type.setItemText(0, QCoreApplication.translate("TabPreview", u"Vertical Only", None))
        self.comboBox_line_type.setItemText(1, QCoreApplication.translate("TabPreview", u"Horizontal Only", None))
        self.comboBox_line_type.setItemText(2, QCoreApplication.translate("TabPreview", u"All Lines", None))

#if QT_CONFIG(tooltip)
        self.comboBox_line_type.setToolTip(QCoreApplication.translate("TabPreview", u"<html><head/><body><p>Preview lines for which direction.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox.setTitle(QCoreApplication.translate("TabPreview", u"Image Settings", None))
#if QT_CONFIG(tooltip)
        self.checkBox_live_preview.setToolTip(QCoreApplication.translate("TabPreview", u"<html><head/><body><p>Automatically preview screen region when update location.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_live_preview.setText(QCoreApplication.translate("TabPreview", u"Live Prev.", None))
#if QT_CONFIG(tooltip)
        self.pushButton_update_image.setToolTip(QCoreApplication.translate("TabPreview", u"<html><head/><body><p>Capture and update preview form the located region.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_update_image.setText(QCoreApplication.translate("TabPreview", u"Update", None))
#if QT_CONFIG(tooltip)
        self.checkBox_save_preview.setToolTip(QCoreApplication.translate("TabPreview", u"<html><head/><body><p>Save preview.jpg to working dir.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_save_preview.setText(QCoreApplication.translate("TabPreview", u"Save Prev.", None))
#if QT_CONFIG(tooltip)
        self.pushButton_glob_image.setToolTip(QCoreApplication.translate("TabPreview", u"<html><head/><body><p><span style=\" font-family:'quote-cjk-patch','Inter','system-ui','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Open Sans','Helvetica Neue','sans-serif'; font-size:16px; color:#0f1115; background-color:#ffffff;\">Preview images matching a glob wildcard pattern.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_glob_image.setText(QCoreApplication.translate("TabPreview", u"Filter", None))
#if QT_CONFIG(tooltip)
        self.pushButton_invert_image.setToolTip(QCoreApplication.translate("TabPreview", u"<html><head/><body><p><span style=\" font-family:'quote-cjk-patch','Inter','system-ui','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Oxygen','Ubuntu','Cantarell','Open Sans','Helvetica Neue','sans-serif'; font-size:16px; color:#0f1115; background-color:#ffffff;\">Converts image to its complementary colors.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_invert_image.setText(QCoreApplication.translate("TabPreview", u"Invert", None))
#if QT_CONFIG(tooltip)
        self.pushButton_open_image.setToolTip(QCoreApplication.translate("TabPreview", u"<html><head/><body><p>Select and open one or more image files for preview.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_open_image.setText(QCoreApplication.translate("TabPreview", u"Open", None))
    # retranslateUi

