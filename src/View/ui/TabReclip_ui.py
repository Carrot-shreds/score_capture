# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TabReclip.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QSpinBox, QSplitter, QWidget)

from ..widgets.ImageViewer import ImageViewer

class Ui_TabReclip(object):
    def setupUi(self, TabReclip):
        if not TabReclip.objectName():
            TabReclip.setObjectName(u"TabReclip")
        TabReclip.resize(731, 585)
        self.horizontalLayout = QHBoxLayout(TabReclip)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter = QSplitter(TabReclip)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.scrollArea = QScrollArea(self.splitter)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 513, 565))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_20 = QLabel(self.scrollAreaWidgetContents)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_20, 4, 0, 1, 1)

        self.label_23 = QLabel(self.scrollAreaWidgetContents)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_23.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_23, 8, 0, 1, 1)

        self.label_26 = QLabel(self.scrollAreaWidgetContents)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_26.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_26, 14, 0, 1, 1)

        self.label_24 = QLabel(self.scrollAreaWidgetContents)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_24.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_24, 12, 0, 1, 1)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_2, 11, 0, 1, 1)

        self.label_27 = QLabel(self.scrollAreaWidgetContents)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_27.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_27, 15, 0, 1, 1)

        self.label_21 = QLabel(self.scrollAreaWidgetContents)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_21, 5, 0, 1, 1)

        self.pushButton_open_style = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_open_style.setObjectName(u"pushButton_open_style")

        self.gridLayout.addWidget(self.pushButton_open_style, 17, 0, 1, 1)

        self.checkBox_live_preview = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_live_preview.setObjectName(u"checkBox_live_preview")

        self.gridLayout.addWidget(self.checkBox_live_preview, 9, 3, 1, 1)

        self.label_28 = QLabel(self.scrollAreaWidgetContents)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_28.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_28, 13, 0, 1, 1)

        self.comboBox_clip_align = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_clip_align.addItem("")
        self.comboBox_clip_align.addItem("")
        self.comboBox_clip_align.addItem("")
        self.comboBox_clip_align.setObjectName(u"comboBox_clip_align")

        self.gridLayout.addWidget(self.comboBox_clip_align, 6, 3, 1, 1)

        self.label_18 = QLabel(self.scrollAreaWidgetContents)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_18, 1, 0, 1, 1)

        self.checkBox_clip_resize = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_clip_resize.setObjectName(u"checkBox_clip_resize")

        self.gridLayout.addWidget(self.checkBox_clip_resize, 9, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 18, 0, 1, 1)

        self.doubleSpinBox_margin_width = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.doubleSpinBox_margin_width.setObjectName(u"doubleSpinBox_margin_width")
        self.doubleSpinBox_margin_width.setDecimals(2)
        self.doubleSpinBox_margin_width.setMinimum(0.010000000000000)
        self.doubleSpinBox_margin_width.setMaximum(0.300000000000000)
        self.doubleSpinBox_margin_width.setSingleStep(0.010000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_margin_width, 14, 3, 1, 1)

        self.doubleSpinBox_resize_threshold = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.doubleSpinBox_resize_threshold.setObjectName(u"doubleSpinBox_resize_threshold")
        self.doubleSpinBox_resize_threshold.setDecimals(1)
        self.doubleSpinBox_resize_threshold.setMinimum(0.100000000000000)
        self.doubleSpinBox_resize_threshold.setMaximum(0.900000000000000)
        self.doubleSpinBox_resize_threshold.setSingleStep(0.100000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_resize_threshold, 8, 3, 1, 1)

        self.pushButton_reclip = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_reclip.setObjectName(u"pushButton_reclip")

        self.gridLayout.addWidget(self.pushButton_reclip, 0, 0, 1, 1)

        self.label_19 = QLabel(self.scrollAreaWidgetContents)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_19.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_19, 6, 0, 1, 1)

        self.pushButton_show_style = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_show_style.setObjectName(u"pushButton_show_style")

        self.gridLayout.addWidget(self.pushButton_show_style, 0, 3, 1, 1)

        self.doubleSpinBox_margin_height = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.doubleSpinBox_margin_height.setObjectName(u"doubleSpinBox_margin_height")
        self.doubleSpinBox_margin_height.setDecimals(2)
        self.doubleSpinBox_margin_height.setMinimum(0.010000000000000)
        self.doubleSpinBox_margin_height.setMaximum(0.300000000000000)
        self.doubleSpinBox_margin_height.setSingleStep(0.010000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_margin_height, 15, 3, 1, 1)

        self.spinBox_clip_margin = QSpinBox(self.scrollAreaWidgetContents)
        self.spinBox_clip_margin.setObjectName(u"spinBox_clip_margin")

        self.gridLayout.addWidget(self.spinBox_clip_margin, 2, 3, 1, 1)

        self.pushButton_save_style = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_save_style.setObjectName(u"pushButton_save_style")

        self.gridLayout.addWidget(self.pushButton_save_style, 17, 3, 1, 1)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 11, 3, 1, 1)

        self.label_22 = QLabel(self.scrollAreaWidgetContents)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_22.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_22, 2, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 18, 3, 1, 1)

        self.lineEdit_title = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_title.setObjectName(u"lineEdit_title")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit_title.sizePolicy().hasHeightForWidth())
        self.lineEdit_title.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.lineEdit_title, 12, 3, 1, 1)

        self.doubleSpinBox_margin_title = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.doubleSpinBox_margin_title.setObjectName(u"doubleSpinBox_margin_title")
        self.doubleSpinBox_margin_title.setDecimals(2)
        self.doubleSpinBox_margin_title.setMinimum(0.010000000000000)
        self.doubleSpinBox_margin_title.setMaximum(0.300000000000000)
        self.doubleSpinBox_margin_title.setSingleStep(0.010000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_margin_title, 13, 3, 1, 1)

        self.comboBox_reclip_method = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_reclip_method.addItem("")
        self.comboBox_reclip_method.addItem("")
        self.comboBox_reclip_method.setObjectName(u"comboBox_reclip_method")

        self.gridLayout.addWidget(self.comboBox_reclip_method, 1, 3, 1, 1)

        self.spinBox_each_line_bar_num = QSpinBox(self.scrollAreaWidgetContents)
        self.spinBox_each_line_bar_num.setObjectName(u"spinBox_each_line_bar_num")

        self.gridLayout.addWidget(self.spinBox_each_line_bar_num, 4, 3, 1, 1)

        self.spinBox_each_line_ength = QSpinBox(self.scrollAreaWidgetContents)
        self.spinBox_each_line_ength.setObjectName(u"spinBox_each_line_ength")

        self.gridLayout.addWidget(self.spinBox_each_line_ength, 5, 3, 1, 1)

        self.label_29 = QLabel(self.scrollAreaWidgetContents)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_29.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_29, 16, 0, 1, 1)

        self.comboBox_font_name = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_font_name.setObjectName(u"comboBox_font_name")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboBox_font_name.sizePolicy().hasHeightForWidth())
        self.comboBox_font_name.setSizePolicy(sizePolicy2)
        self.comboBox_font_name.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)

        self.gridLayout.addWidget(self.comboBox_font_name, 16, 3, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.splitter.addWidget(self.scrollArea)
        self.ImageViewer = ImageViewer(self.splitter)
        self.ImageViewer.setObjectName(u"ImageViewer")
        self.splitter.addWidget(self.ImageViewer)

        self.horizontalLayout.addWidget(self.splitter)


        self.retranslateUi(TabReclip)

        QMetaObject.connectSlotsByName(TabReclip)
    # setupUi

    def retranslateUi(self, TabReclip):
        TabReclip.setWindowTitle(QCoreApplication.translate("TabReclip", u"Form", None))
        self.label_20.setText(QCoreApplication.translate("TabReclip", u"\u5355\u884c\u5c0f\u8282\u6570\uff1a", None))
        self.label_23.setText(QCoreApplication.translate("TabReclip", u"\u7f29\u653e\u9608\u503c\uff1a", None))
        self.label_26.setText(QCoreApplication.translate("TabReclip", u"\u6a2a\u5411\u8fb9\u8ddd\uff1a", None))
        self.label_24.setText(QCoreApplication.translate("TabReclip", u"\u6807\u9898\uff1a", None))
        self.label_27.setText(QCoreApplication.translate("TabReclip", u"\u7eb5\u5411\u8fb9\u8ddd\uff1a", None))
        self.label_21.setText(QCoreApplication.translate("TabReclip", u"\u5355\u884c\u957f\u5ea6\uff1a", None))
        self.pushButton_open_style.setText(QCoreApplication.translate("TabReclip", u"\u6253\u5f00\u6837\u5f0f", None))
        self.checkBox_live_preview.setText(QCoreApplication.translate("TabReclip", u"\u5b9e\u65f6\u9884\u89c8", None))
        self.label_28.setText(QCoreApplication.translate("TabReclip", u"\u6807\u9898\u9ad8\u5ea6\uff1a", None))
        self.comboBox_clip_align.setItemText(0, QCoreApplication.translate("TabReclip", u"\u5c45\u5de6", None))
        self.comboBox_clip_align.setItemText(1, QCoreApplication.translate("TabReclip", u"\u5c45\u4e2d", None))
        self.comboBox_clip_align.setItemText(2, QCoreApplication.translate("TabReclip", u"\u5c45\u53f3", None))

        self.comboBox_clip_align.setCurrentText(QCoreApplication.translate("TabReclip", u"\u5c45\u5de6", None))
        self.label_18.setText(QCoreApplication.translate("TabReclip", u"\u5206\u5272\u6a21\u5f0f\uff1a", None))
        self.checkBox_clip_resize.setText(QCoreApplication.translate("TabReclip", u"\u5207\u7247\u7f29\u653e", None))
        self.pushButton_reclip.setText(QCoreApplication.translate("TabReclip", u"\u6267\u884c\u91cd\u5206\u5272", None))
        self.label_19.setText(QCoreApplication.translate("TabReclip", u"\u5207\u7247\u5bf9\u9f50\uff1a", None))
        self.pushButton_show_style.setText(QCoreApplication.translate("TabReclip", u"\u66f4\u65b0\u6837\u5f0f", None))
        self.pushButton_save_style.setText(QCoreApplication.translate("TabReclip", u"\u53e6\u5b58\u6837\u5f0f", None))
        self.label_22.setText(QCoreApplication.translate("TabReclip", u"\u5207\u7247\u5916\u8fb9\u8ddd\uff1a", None))
        self.comboBox_reclip_method.setItemText(0, QCoreApplication.translate("TabReclip", u"\u56fa\u5b9a\u5c0f\u8282", None))
        self.comboBox_reclip_method.setItemText(1, QCoreApplication.translate("TabReclip", u"\u9650\u5236\u5bbd\u5ea6", None))

        self.comboBox_reclip_method.setCurrentText(QCoreApplication.translate("TabReclip", u"\u56fa\u5b9a\u5c0f\u8282", None))
        self.label_29.setText(QCoreApplication.translate("TabReclip", u"\u5b57\u4f53\u540d\u79f0\uff1a", None))
    # retranslateUi

