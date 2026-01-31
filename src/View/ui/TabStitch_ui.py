# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TabStitch.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QDoubleSpinBox, QHBoxLayout, QLabel, QPushButton,
    QRadioButton, QSizePolicy, QSpinBox, QSplitter,
    QTabWidget, QVBoxLayout, QWidget)

from ..widgets.ImageViewer import ImageViewer

class Ui_TabStitch(object):
    def setupUi(self, TabStitch):
        if not TabStitch.objectName():
            TabStitch.setObjectName(u"TabStitch")
        TabStitch.resize(902, 300)
        self.verticalLayout_2 = QVBoxLayout(TabStitch)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.splitter = QSplitter(TabStitch)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.setHandleWidth(10)
        self.splitter.setChildrenCollapsible(False)
        self.tabWidget = QTabWidget(self.splitter)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tab_auto = QWidget()
        self.tab_auto.setObjectName(u"tab_auto")
        self.horizontalLayout = QHBoxLayout(self.tab_auto)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_17 = QLabel(self.tab_auto)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_17)

        self.comboBox_stitch_method = QComboBox(self.tab_auto)
        self.comboBox_stitch_method.addItem("")
        self.comboBox_stitch_method.addItem("")
        self.comboBox_stitch_method.addItem("")
        self.comboBox_stitch_method.setObjectName(u"comboBox_stitch_method")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_stitch_method.sizePolicy().hasHeightForWidth())
        self.comboBox_stitch_method.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.comboBox_stitch_method)

        self.label_27 = QLabel(self.tab_auto)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_27)

        self.radioButton_stitch_direction_vertical = QRadioButton(self.tab_auto)
        self.radioButton_stitch_direction_vertical.setObjectName(u"radioButton_stitch_direction_vertical")

        self.horizontalLayout.addWidget(self.radioButton_stitch_direction_vertical)

        self.radioButton_stitch_direction_horizontal = QRadioButton(self.tab_auto)
        self.radioButton_stitch_direction_horizontal.setObjectName(u"radioButton_stitch_direction_horizontal")

        self.horizontalLayout.addWidget(self.radioButton_stitch_direction_horizontal)

        self.pushButton_start_stitiching = QPushButton(self.tab_auto)
        self.pushButton_start_stitiching.setObjectName(u"pushButton_start_stitiching")

        self.horizontalLayout.addWidget(self.pushButton_start_stitiching)

        self.tabWidget.addTab(self.tab_auto, "")
        self.tab_manual = QWidget()
        self.tab_manual.setObjectName(u"tab_manual")
        self.horizontalLayout_3 = QHBoxLayout(self.tab_manual)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.tab_manual)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label)

        self.spinBox_stitch_points_index = QSpinBox(self.tab_manual)
        self.spinBox_stitch_points_index.setObjectName(u"spinBox_stitch_points_index")

        self.horizontalLayout_3.addWidget(self.spinBox_stitch_points_index)

        self.label_2 = QLabel(self.tab_manual)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.spinBox_stitch_points_value = QSpinBox(self.tab_manual)
        self.spinBox_stitch_points_value.setObjectName(u"spinBox_stitch_points_value")
        self.spinBox_stitch_points_value.setStepType(QAbstractSpinBox.StepType.DefaultStepType)

        self.horizontalLayout_3.addWidget(self.spinBox_stitch_points_value)

        self.label_3 = QLabel(self.tab_manual)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.pushButton_select_file = QPushButton(self.tab_manual)
        self.pushButton_select_file.setObjectName(u"pushButton_select_file")

        self.horizontalLayout_3.addWidget(self.pushButton_select_file)

        self.pushButton_save_file = QPushButton(self.tab_manual)
        self.pushButton_save_file.setObjectName(u"pushButton_save_file")

        self.horizontalLayout_3.addWidget(self.pushButton_save_file)

        self.pushButton_save_file_as = QPushButton(self.tab_manual)
        self.pushButton_save_file_as.setObjectName(u"pushButton_save_file_as")

        self.horizontalLayout_3.addWidget(self.pushButton_save_file_as)

        self.pushButton_save_image = QPushButton(self.tab_manual)
        self.pushButton_save_image.setObjectName(u"pushButton_save_image")

        self.horizontalLayout_3.addWidget(self.pushButton_save_image)

        self.tabWidget.addTab(self.tab_manual, "")
        self.tab_view = QWidget()
        self.tab_view.setObjectName(u"tab_view")
        self.horizontalLayout_2 = QHBoxLayout(self.tab_view)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBox_lock_zoom = QCheckBox(self.tab_view)
        self.checkBox_lock_zoom.setObjectName(u"checkBox_lock_zoom")

        self.horizontalLayout_2.addWidget(self.checkBox_lock_zoom)

        self.checkBox_show_mark_point = QCheckBox(self.tab_view)
        self.checkBox_show_mark_point.setObjectName(u"checkBox_show_mark_point")

        self.horizontalLayout_2.addWidget(self.checkBox_show_mark_point)

        self.label_4 = QLabel(self.tab_view)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_4)

        self.doubleSpinBox_location_mark_point = QDoubleSpinBox(self.tab_view)
        self.doubleSpinBox_location_mark_point.setObjectName(u"doubleSpinBox_location_mark_point")
        self.doubleSpinBox_location_mark_point.setMinimum(0.100000000000000)
        self.doubleSpinBox_location_mark_point.setMaximum(1.000000000000000)
        self.doubleSpinBox_location_mark_point.setSingleStep(0.010000000000000)
        self.doubleSpinBox_location_mark_point.setValue(0.350000000000000)

        self.horizontalLayout_2.addWidget(self.doubleSpinBox_location_mark_point)

        self.tabWidget.addTab(self.tab_view, "")
        self.splitter.addWidget(self.tabWidget)
        self.ImageViewer = ImageViewer(self.splitter)
        self.ImageViewer.setObjectName(u"ImageViewer")
        self.splitter.addWidget(self.ImageViewer)

        self.verticalLayout_2.addWidget(self.splitter)


        self.retranslateUi(TabStitch)

        self.tabWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(TabStitch)
    # setupUi

    def retranslateUi(self, TabStitch):
        TabStitch.setWindowTitle(QCoreApplication.translate("TabStitch", u"Form", None))
        self.label_17.setText(QCoreApplication.translate("TabStitch", u"\u62fc\u63a5\u70b9\u7b97\u6cd5\uff1a", None))
        self.comboBox_stitch_method.setItemText(0, QCoreApplication.translate("TabStitch", u"MSE", None))
        self.comboBox_stitch_method.setItemText(1, QCoreApplication.translate("TabStitch", u"SSIM", None))
        self.comboBox_stitch_method.setItemText(2, QCoreApplication.translate("TabStitch", u"DIRECT", None))

        self.comboBox_stitch_method.setCurrentText(QCoreApplication.translate("TabStitch", u"MSE", None))
        self.label_27.setText(QCoreApplication.translate("TabStitch", u"\u62fc\u63a5\u65b9\u5411\uff1a", None))
        self.radioButton_stitch_direction_vertical.setText(QCoreApplication.translate("TabStitch", u"\u7eb5\u5411", None))
        self.radioButton_stitch_direction_horizontal.setText(QCoreApplication.translate("TabStitch", u"\u6a2a\u5411", None))
        self.pushButton_start_stitiching.setText(QCoreApplication.translate("TabStitch", u"\u5f00\u59cb\u62fc\u63a5", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_auto), QCoreApplication.translate("TabStitch", u"\u81ea\u52a8\u62fc\u63a5", None))
        self.label.setText(QCoreApplication.translate("TabStitch", u"\u62fc\u63a5\u70b9\u5e8f\u53f7\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("TabStitch", u"\u504f\u79fb\u50cf\u7d20\u503c\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("TabStitch", u"\u62fc\u63a5\u70b9\u6570\u636e\uff1a", None))
        self.pushButton_select_file.setText(QCoreApplication.translate("TabStitch", u"\u6253\u5f00\u6587\u4ef6", None))
        self.pushButton_save_file.setText(QCoreApplication.translate("TabStitch", u"\u4fdd\u5b58", None))
        self.pushButton_save_file_as.setText(QCoreApplication.translate("TabStitch", u"\u53e6\u5b58\u4e3a", None))
        self.pushButton_save_image.setText(QCoreApplication.translate("TabStitch", u"\u4fdd\u5b58\u62fc\u63a5\u56fe\u50cf", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_manual), QCoreApplication.translate("TabStitch", u"\u624b\u52a8\u8c03\u6574", None))
        self.checkBox_lock_zoom.setText(QCoreApplication.translate("TabStitch", u"\u9501\u5b9a\u7f29\u653e", None))
        self.checkBox_show_mark_point.setText(QCoreApplication.translate("TabStitch", u"\u9884\u89c8\u663e\u793a\u6807\u8bb0\u70b9", None))
        self.label_4.setText(QCoreApplication.translate("TabStitch", u"\u6807\u8bb0\u70b9\u4f4d\u7f6e\uff1a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_view), QCoreApplication.translate("TabStitch", u"\u89c6\u56fe/\u64cd\u4f5c", None))
    # retranslateUi

