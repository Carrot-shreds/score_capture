# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stitch.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

from pyqtgraph import ImageView

class Ui_Widget_Stitch(object):
    def setupUi(self, Widget_Stitch):
        if not Widget_Stitch.objectName():
            Widget_Stitch.setObjectName(u"Widget_Stitch")
        Widget_Stitch.resize(855, 246)
        self.verticalLayout = QVBoxLayout(Widget_Stitch)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(379, 21, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label = QLabel(Widget_Stitch)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.spinBox_stitch_points_index = QSpinBox(Widget_Stitch)
        self.spinBox_stitch_points_index.setObjectName(u"spinBox_stitch_points_index")

        self.horizontalLayout.addWidget(self.spinBox_stitch_points_index)

        self.label_2 = QLabel(Widget_Stitch)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.spinBox_stitch_points_value = QSpinBox(Widget_Stitch)
        self.spinBox_stitch_points_value.setObjectName(u"spinBox_stitch_points_value")
        self.spinBox_stitch_points_value.setStepType(QAbstractSpinBox.StepType.DefaultStepType)

        self.horizontalLayout.addWidget(self.spinBox_stitch_points_value)

        self.horizontalSpacer_3 = QSpacerItem(379, 21, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.label_3 = QLabel(Widget_Stitch)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.pushButton_open_file = QPushButton(Widget_Stitch)
        self.pushButton_open_file.setObjectName(u"pushButton_open_file")

        self.horizontalLayout.addWidget(self.pushButton_open_file)

        self.pushButton_save_file = QPushButton(Widget_Stitch)
        self.pushButton_save_file.setObjectName(u"pushButton_save_file")

        self.horizontalLayout.addWidget(self.pushButton_save_file)

        self.horizontalSpacer_4 = QSpacerItem(379, 21, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.pushButton_save_image = QPushButton(Widget_Stitch)
        self.pushButton_save_image.setObjectName(u"pushButton_save_image")

        self.horizontalLayout.addWidget(self.pushButton_save_image)

        self.horizontalSpacer_2 = QSpacerItem(379, 21, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.graphWidget = ImageView(Widget_Stitch)
        self.graphWidget.setObjectName(u"graphWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphWidget.sizePolicy().hasHeightForWidth())
        self.graphWidget.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.graphWidget)


        self.retranslateUi(Widget_Stitch)

        QMetaObject.connectSlotsByName(Widget_Stitch)
    # setupUi

    def retranslateUi(self, Widget_Stitch):
        Widget_Stitch.setWindowTitle(QCoreApplication.translate("Widget_Stitch", u"Stitch Manually", None))
        self.label.setText(QCoreApplication.translate("Widget_Stitch", u"\u62fc\u63a5\u70b9\u5e8f\u53f7", None))
        self.label_2.setText(QCoreApplication.translate("Widget_Stitch", u"\u504f\u79fb\u50cf\u7d20\u503c", None))
        self.label_3.setText(QCoreApplication.translate("Widget_Stitch", u"\u62fc\u63a5\u70b9\u6570\u636e", None))
        self.pushButton_open_file.setText(QCoreApplication.translate("Widget_Stitch", u"\u6253\u5f00", None))
        self.pushButton_save_file.setText(QCoreApplication.translate("Widget_Stitch", u"\u4fdd\u5b58", None))
        self.pushButton_save_image.setText(QCoreApplication.translate("Widget_Stitch", u"\u4fdd\u5b58\u62fc\u63a5\u56fe\u50cf", None))
    # retranslateUi

