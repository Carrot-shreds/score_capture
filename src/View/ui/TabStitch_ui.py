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
    QDoubleSpinBox, QFrame, QHBoxLayout, QLabel,
    QPushButton, QRadioButton, QSizePolicy, QSpinBox,
    QSplitter, QTabWidget, QVBoxLayout, QWidget)

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

        self.line_5 = QFrame(self.tab_auto)
        self.line_5.setObjectName(u"line_5")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.line_5.sizePolicy().hasHeightForWidth())
        self.line_5.setSizePolicy(sizePolicy1)
        self.line_5.setMinimumSize(QSize(0, 30))
        self.line_5.setFrameShape(QFrame.Shape.VLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line_5)

        self.label_27 = QLabel(self.tab_auto)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_27)

        self.radioButton_stitch_direction_vertical = QRadioButton(self.tab_auto)
        self.radioButton_stitch_direction_vertical.setObjectName(u"radioButton_stitch_direction_vertical")
        sizePolicy1.setHeightForWidth(self.radioButton_stitch_direction_vertical.sizePolicy().hasHeightForWidth())
        self.radioButton_stitch_direction_vertical.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.radioButton_stitch_direction_vertical)

        self.radioButton_stitch_direction_horizontal = QRadioButton(self.tab_auto)
        self.radioButton_stitch_direction_horizontal.setObjectName(u"radioButton_stitch_direction_horizontal")
        sizePolicy1.setHeightForWidth(self.radioButton_stitch_direction_horizontal.sizePolicy().hasHeightForWidth())
        self.radioButton_stitch_direction_horizontal.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.radioButton_stitch_direction_horizontal)

        self.line_4 = QFrame(self.tab_auto)
        self.line_4.setObjectName(u"line_4")
        sizePolicy1.setHeightForWidth(self.line_4.sizePolicy().hasHeightForWidth())
        self.line_4.setSizePolicy(sizePolicy1)
        self.line_4.setMinimumSize(QSize(0, 30))
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line_4)

        self.pushButton_start_stitiching = QPushButton(self.tab_auto)
        self.pushButton_start_stitiching.setObjectName(u"pushButton_start_stitiching")

        self.horizontalLayout.addWidget(self.pushButton_start_stitiching)

        self.pushButton_clear_cache = QPushButton(self.tab_auto)
        self.pushButton_clear_cache.setObjectName(u"pushButton_clear_cache")

        self.horizontalLayout.addWidget(self.pushButton_clear_cache)

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
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.spinBox_stitch_points_value = QSpinBox(self.tab_manual)
        self.spinBox_stitch_points_value.setObjectName(u"spinBox_stitch_points_value")
        self.spinBox_stitch_points_value.setStepType(QAbstractSpinBox.StepType.DefaultStepType)

        self.horizontalLayout_3.addWidget(self.spinBox_stitch_points_value)

        self.line = QFrame(self.tab_manual)
        self.line.setObjectName(u"line")
        sizePolicy1.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy1)
        self.line.setMinimumSize(QSize(0, 40))
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_3.addWidget(self.line)

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

        self.line_2 = QFrame(self.tab_manual)
        self.line_2.setObjectName(u"line_2")
        sizePolicy1.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy1)
        self.line_2.setMinimumSize(QSize(0, 40))
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_3.addWidget(self.line_2)

        self.pushButton_save_image = QPushButton(self.tab_manual)
        self.pushButton_save_image.setObjectName(u"pushButton_save_image")

        self.horizontalLayout_3.addWidget(self.pushButton_save_image)

        self.tabWidget.addTab(self.tab_manual, "")
        self.tab_view = QWidget()
        self.tab_view.setObjectName(u"tab_view")
        self.horizontalLayout_6 = QHBoxLayout(self.tab_view)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_4 = QLabel(self.tab_view)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.label_4)

        self.doubleSpinBox_location_mark_point = QDoubleSpinBox(self.tab_view)
        self.doubleSpinBox_location_mark_point.setObjectName(u"doubleSpinBox_location_mark_point")
        self.doubleSpinBox_location_mark_point.setMinimum(0.100000000000000)
        self.doubleSpinBox_location_mark_point.setMaximum(1.000000000000000)
        self.doubleSpinBox_location_mark_point.setSingleStep(0.010000000000000)
        self.doubleSpinBox_location_mark_point.setValue(0.350000000000000)

        self.horizontalLayout_6.addWidget(self.doubleSpinBox_location_mark_point)

        self.checkBox_show_mark_point = QCheckBox(self.tab_view)
        self.checkBox_show_mark_point.setObjectName(u"checkBox_show_mark_point")

        self.horizontalLayout_6.addWidget(self.checkBox_show_mark_point)

        self.line_3 = QFrame(self.tab_view)
        self.line_3.setObjectName(u"line_3")
        sizePolicy1.setHeightForWidth(self.line_3.sizePolicy().hasHeightForWidth())
        self.line_3.setSizePolicy(sizePolicy1)
        self.line_3.setMinimumSize(QSize(0, 30))
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_6.addWidget(self.line_3)

        self.checkBox_lock_zoom = QCheckBox(self.tab_view)
        self.checkBox_lock_zoom.setObjectName(u"checkBox_lock_zoom")

        self.horizontalLayout_6.addWidget(self.checkBox_lock_zoom)

        self.checkBox_auto_zoom = QCheckBox(self.tab_view)
        self.checkBox_auto_zoom.setObjectName(u"checkBox_auto_zoom")

        self.horizontalLayout_6.addWidget(self.checkBox_auto_zoom)

        self.pushButton_reset_region = QPushButton(self.tab_view)
        self.pushButton_reset_region.setObjectName(u"pushButton_reset_region")

        self.horizontalLayout_6.addWidget(self.pushButton_reset_region)

        self.tabWidget.addTab(self.tab_view, "")
        self.splitter.addWidget(self.tabWidget)
        self.ImageViewer = ImageViewer(self.splitter)
        self.ImageViewer.setObjectName(u"ImageViewer")
        self.splitter.addWidget(self.ImageViewer)

        self.verticalLayout_2.addWidget(self.splitter)


        self.retranslateUi(TabStitch)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(TabStitch)
    # setupUi

    def retranslateUi(self, TabStitch):
        TabStitch.setWindowTitle(QCoreApplication.translate("TabStitch", u"Form", None))
        self.label_17.setText(QCoreApplication.translate("TabStitch", u"Stitch Method:", None))
        self.comboBox_stitch_method.setItemText(0, QCoreApplication.translate("TabStitch", u"MSE", None))
        self.comboBox_stitch_method.setItemText(1, QCoreApplication.translate("TabStitch", u"SSIM", None))
        self.comboBox_stitch_method.setItemText(2, QCoreApplication.translate("TabStitch", u"DIRECT", None))

#if QT_CONFIG(tooltip)
        self.comboBox_stitch_method.setToolTip(QCoreApplication.translate("TabStitch", u"<html><head/><body><p>SSIM: A bit slower but have way better result. Recommended.</p><p>MSE: Less cpu usage.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_stitch_method.setCurrentText(QCoreApplication.translate("TabStitch", u"MSE", None))
        self.label_27.setText(QCoreApplication.translate("TabStitch", u"Stitch Direction:", None))
        self.radioButton_stitch_direction_vertical.setText(QCoreApplication.translate("TabStitch", u"Vertical", None))
        self.radioButton_stitch_direction_horizontal.setText(QCoreApplication.translate("TabStitch", u"Horizontal", None))
        self.pushButton_start_stitiching.setText(QCoreApplication.translate("TabStitch", u"Start Stitch", None))
#if QT_CONFIG(tooltip)
        self.pushButton_clear_cache.setToolTip(QCoreApplication.translate("TabStitch", u"<html><head/><body><p>Remove ScoreDetections.json which cached detected lines data, used to stitch images as reference.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_clear_cache.setText(QCoreApplication.translate("TabStitch", u"Clear Line Cache", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_auto), QCoreApplication.translate("TabStitch", u"Auto", None))
        self.label.setText(QCoreApplication.translate("TabStitch", u"Index:", None))
#if QT_CONFIG(tooltip)
        self.spinBox_stitch_points_index.setToolTip(QCoreApplication.translate("TabStitch", u"<html><head/><body><p>The index of stitch points.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("TabStitch", u"Position:", None))
#if QT_CONFIG(tooltip)
        self.spinBox_stitch_points_value.setToolTip(QCoreApplication.translate("TabStitch", u"<html><head/><body><p>The value of the stitch point.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("TabStitch", u"ScoreStitchData:", None))
        self.pushButton_select_file.setText(QCoreApplication.translate("TabStitch", u"Open", None))
        self.pushButton_save_file.setText(QCoreApplication.translate("TabStitch", u"Save", None))
        self.pushButton_save_file_as.setText(QCoreApplication.translate("TabStitch", u"Save As", None))
#if QT_CONFIG(tooltip)
        self.pushButton_save_image.setToolTip(QCoreApplication.translate("TabStitch", u"<html><head/><body><p>Save manual stitched image to reclip.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_save_image.setText(QCoreApplication.translate("TabStitch", u"Save Image", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_manual), QCoreApplication.translate("TabStitch", u"Manual", None))
        self.label_4.setText(QCoreApplication.translate("TabStitch", u"Mark Point Position:", None))
#if QT_CONFIG(tooltip)
        self.doubleSpinBox_location_mark_point.setToolTip(QCoreApplication.translate("TabStitch", u"<html><head/><body><p>Position of the mark point. From 0 to 1 on the stitching line axis.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_show_mark_point.setText(QCoreApplication.translate("TabStitch", u"Show Mark Point", None))
#if QT_CONFIG(tooltip)
        self.checkBox_lock_zoom.setToolTip(QCoreApplication.translate("TabStitch", u"<html><head/><body><p>Lock the view zoom in the opposite direction of stitch direction.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_lock_zoom.setText(QCoreApplication.translate("TabStitch", u"Lock Zoom", None))
#if QT_CONFIG(tooltip)
        self.checkBox_auto_zoom.setToolTip(QCoreApplication.translate("TabStitch", u"<html><head/><body><p>Auto reset zoom and range when index or position changed.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_auto_zoom.setText(QCoreApplication.translate("TabStitch", u"Auto Range", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_region.setToolTip(QCoreApplication.translate("TabStitch", u"<html><head/><body><p>Reset the preview region to current stitching line area.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_region.setText(QCoreApplication.translate("TabStitch", u"Reset Zoom", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_view), QCoreApplication.translate("TabStitch", u"View", None))
    # retranslateUi

