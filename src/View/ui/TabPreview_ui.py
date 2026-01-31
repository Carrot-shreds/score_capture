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
    QLabel, QPushButton, QSizePolicy, QSplitter,
    QVBoxLayout, QWidget)

from ..widgets.ImageViewer import ImageViewer

class Ui_TabPreview(object):
    def setupUi(self, TabPreview):
        if not TabPreview.objectName():
            TabPreview.setObjectName(u"TabPreview")
        TabPreview.resize(1096, 281)
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
        self.label_detect_coefficient_horizontal = QLabel(self.groupBox_detect_coefficients)
        self.label_detect_coefficient_horizontal.setObjectName(u"label_detect_coefficient_horizontal")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_detect_coefficient_horizontal.sizePolicy().hasHeightForWidth())
        self.label_detect_coefficient_horizontal.setSizePolicy(sizePolicy2)
        self.label_detect_coefficient_horizontal.setMinimumSize(QSize(0, 0))
        self.label_detect_coefficient_horizontal.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_detect_coefficient_horizontal, 0, 0, 1, 1)

        self.doubleSpinBox_detect_coefficient_horizontal = QDoubleSpinBox(self.groupBox_detect_coefficients)
        self.doubleSpinBox_detect_coefficient_horizontal.setObjectName(u"doubleSpinBox_detect_coefficient_horizontal")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.doubleSpinBox_detect_coefficient_horizontal.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_detect_coefficient_horizontal.setSizePolicy(sizePolicy3)
        self.doubleSpinBox_detect_coefficient_horizontal.setMaximum(100.000000000000000)
        self.doubleSpinBox_detect_coefficient_horizontal.setSingleStep(0.010000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_detect_coefficient_horizontal, 0, 1, 1, 1)

        self.label_detect_coefficient_vertical = QLabel(self.groupBox_detect_coefficients)
        self.label_detect_coefficient_vertical.setObjectName(u"label_detect_coefficient_vertical")
        sizePolicy2.setHeightForWidth(self.label_detect_coefficient_vertical.sizePolicy().hasHeightForWidth())
        self.label_detect_coefficient_vertical.setSizePolicy(sizePolicy2)
        self.label_detect_coefficient_vertical.setMinimumSize(QSize(0, 0))
        self.label_detect_coefficient_vertical.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_detect_coefficient_vertical, 1, 0, 1, 1)

        self.doubleSpinBox_detect_coefficient_vertical = QDoubleSpinBox(self.groupBox_detect_coefficients)
        self.doubleSpinBox_detect_coefficient_vertical.setObjectName(u"doubleSpinBox_detect_coefficient_vertical")
        sizePolicy3.setHeightForWidth(self.doubleSpinBox_detect_coefficient_vertical.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_detect_coefficient_vertical.setSizePolicy(sizePolicy3)
        self.doubleSpinBox_detect_coefficient_vertical.setMaximum(100.000000000000000)
        self.doubleSpinBox_detect_coefficient_vertical.setSingleStep(0.010000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_detect_coefficient_vertical, 1, 1, 1, 1)


        self.horizontalLayout_2.addWidget(self.groupBox_detect_coefficients)

        self.groupBox_2 = QGroupBox(self.gridFrame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy1.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy1)
        self.groupBox_2.setFlat(False)
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.checkBox_show_plot = QCheckBox(self.groupBox_2)
        self.checkBox_show_plot.setObjectName(u"checkBox_show_plot")
        sizePolicy3.setHeightForWidth(self.checkBox_show_plot.sizePolicy().hasHeightForWidth())
        self.checkBox_show_plot.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.checkBox_show_plot, 1, 1, 1, 1)

        self.pushButton_detect_lines = QPushButton(self.groupBox_2)
        self.pushButton_detect_lines.setObjectName(u"pushButton_detect_lines")
        sizePolicy3.setHeightForWidth(self.pushButton_detect_lines.sizePolicy().hasHeightForWidth())
        self.pushButton_detect_lines.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.pushButton_detect_lines, 0, 3, 1, 1)

        self.pushButton_clear_lines = QPushButton(self.groupBox_2)
        self.pushButton_clear_lines.setObjectName(u"pushButton_clear_lines")
        sizePolicy3.setHeightForWidth(self.pushButton_clear_lines.sizePolicy().hasHeightForWidth())
        self.pushButton_clear_lines.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.pushButton_clear_lines, 1, 3, 1, 1)

        self.checkBox_live_detect = QCheckBox(self.groupBox_2)
        self.checkBox_live_detect.setObjectName(u"checkBox_live_detect")
        sizePolicy3.setHeightForWidth(self.checkBox_live_detect.sizePolicy().hasHeightForWidth())
        self.checkBox_live_detect.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.checkBox_live_detect, 1, 2, 1, 1)

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

        self.gridLayout_2.addWidget(self.comboBox_line_type, 0, 1, 1, 2)


        self.horizontalLayout_2.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.gridFrame)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFlat(False)
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.checkBox_live_preview = QCheckBox(self.groupBox)
        self.checkBox_live_preview.setObjectName(u"checkBox_live_preview")
        sizePolicy3.setHeightForWidth(self.checkBox_live_preview.sizePolicy().hasHeightForWidth())
        self.checkBox_live_preview.setSizePolicy(sizePolicy3)

        self.gridLayout_3.addWidget(self.checkBox_live_preview, 1, 1, 1, 1)

        self.pushButton_update_image = QPushButton(self.groupBox)
        self.pushButton_update_image.setObjectName(u"pushButton_update_image")
        sizePolicy3.setHeightForWidth(self.pushButton_update_image.sizePolicy().hasHeightForWidth())
        self.pushButton_update_image.setSizePolicy(sizePolicy3)

        self.gridLayout_3.addWidget(self.pushButton_update_image, 0, 1, 1, 1)

        self.checkBox_save_preview = QCheckBox(self.groupBox)
        self.checkBox_save_preview.setObjectName(u"checkBox_save_preview")
        sizePolicy3.setHeightForWidth(self.checkBox_save_preview.sizePolicy().hasHeightForWidth())
        self.checkBox_save_preview.setSizePolicy(sizePolicy3)

        self.gridLayout_3.addWidget(self.checkBox_save_preview, 1, 2, 1, 1)

        self.pushButton_glob_image = QPushButton(self.groupBox)
        self.pushButton_glob_image.setObjectName(u"pushButton_glob_image")
        sizePolicy3.setHeightForWidth(self.pushButton_glob_image.sizePolicy().hasHeightForWidth())
        self.pushButton_glob_image.setSizePolicy(sizePolicy3)

        self.gridLayout_3.addWidget(self.pushButton_glob_image, 1, 3, 1, 1)

        self.pushButton_reverse_image = QPushButton(self.groupBox)
        self.pushButton_reverse_image.setObjectName(u"pushButton_reverse_image")
        sizePolicy3.setHeightForWidth(self.pushButton_reverse_image.sizePolicy().hasHeightForWidth())
        self.pushButton_reverse_image.setSizePolicy(sizePolicy3)

        self.gridLayout_3.addWidget(self.pushButton_reverse_image, 0, 2, 1, 1)

        self.pushButton_open_image = QPushButton(self.groupBox)
        self.pushButton_open_image.setObjectName(u"pushButton_open_image")
        sizePolicy3.setHeightForWidth(self.pushButton_open_image.sizePolicy().hasHeightForWidth())
        self.pushButton_open_image.setSizePolicy(sizePolicy3)

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
        self.groupBox_detect_coefficients.setTitle(QCoreApplication.translate("TabPreview", u"\u7ebf\u6bb5\u8bc6\u522b\u7cfb\u6570", None))
        self.label_detect_coefficient_horizontal.setText(QCoreApplication.translate("TabPreview", u"\u6c34\u5e73\uff1a", None))
        self.label_detect_coefficient_vertical.setText(QCoreApplication.translate("TabPreview", u"\u7ad6\u76f4\uff1a", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("TabPreview", u"\u8bc6\u522b\u8bbe\u7f6e", None))
        self.checkBox_show_plot.setText(QCoreApplication.translate("TabPreview", u"\u663e\u793aplot", None))
        self.pushButton_detect_lines.setText(QCoreApplication.translate("TabPreview", u"\u8bc6\u522b\u7ebf\u6bb5", None))
        self.pushButton_clear_lines.setText(QCoreApplication.translate("TabPreview", u"\u8fd8\u539f\u56fe\u50cf", None))
        self.checkBox_live_detect.setText(QCoreApplication.translate("TabPreview", u"\u5b9e\u65f6\u8bc6\u522b", None))
        self.comboBox_line_type.setItemText(0, QCoreApplication.translate("TabPreview", u"\u4ec5\u6c34\u5e73\u7ebf", None))
        self.comboBox_line_type.setItemText(1, QCoreApplication.translate("TabPreview", u"\u4ec5\u7ad6\u76f4\u7ebf", None))
        self.comboBox_line_type.setItemText(2, QCoreApplication.translate("TabPreview", u"\u6240\u6709\u7ebf\u6bb5", None))

        self.groupBox.setTitle(QCoreApplication.translate("TabPreview", u"\u56fe\u50cf\u8bbe\u7f6e", None))
        self.checkBox_live_preview.setText(QCoreApplication.translate("TabPreview", u"\u5b9e\u65f6\u9884\u89c8", None))
        self.pushButton_update_image.setText(QCoreApplication.translate("TabPreview", u"\u66f4\u65b0\u9884\u89c8", None))
        self.checkBox_save_preview.setText(QCoreApplication.translate("TabPreview", u"\u4fdd\u5b58\u9884\u89c8", None))
        self.pushButton_glob_image.setText(QCoreApplication.translate("TabPreview", u"\u7b5b\u9009\u56fe\u50cf", None))
        self.pushButton_reverse_image.setText(QCoreApplication.translate("TabPreview", u"\u53cd\u8272\u56fe\u50cf", None))
        self.pushButton_open_image.setText(QCoreApplication.translate("TabPreview", u"\u6253\u5f00\u56fe\u50cf", None))
    # retranslateUi

