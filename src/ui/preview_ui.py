# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preview.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QHBoxLayout,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from pyqtgraph import ImageView

class Ui_Widget_Preview(object):
    def setupUi(self, Widget_Preview):
        if not Widget_Preview.objectName():
            Widget_Preview.setObjectName(u"Widget_Preview")
        Widget_Preview.resize(855, 246)
        self.verticalLayout = QVBoxLayout(Widget_Preview)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(379, 21, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_detect_lines = QPushButton(Widget_Preview)
        self.pushButton_detect_lines.setObjectName(u"pushButton_detect_lines")

        self.horizontalLayout.addWidget(self.pushButton_detect_lines)

        self.comboBox = QComboBox(Widget_Preview)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(80, 0))

        self.horizontalLayout.addWidget(self.comboBox)

        self.pushButton_clear_lines = QPushButton(Widget_Preview)
        self.pushButton_clear_lines.setObjectName(u"pushButton_clear_lines")

        self.horizontalLayout.addWidget(self.pushButton_clear_lines)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.pushButton_update_image = QPushButton(Widget_Preview)
        self.pushButton_update_image.setObjectName(u"pushButton_update_image")

        self.horizontalLayout.addWidget(self.pushButton_update_image)

        self.pushButton_reverse_image = QPushButton(Widget_Preview)
        self.pushButton_reverse_image.setObjectName(u"pushButton_reverse_image")

        self.horizontalLayout.addWidget(self.pushButton_reverse_image)

        self.checkBox_save_preview = QCheckBox(Widget_Preview)
        self.checkBox_save_preview.setObjectName(u"checkBox_save_preview")

        self.horizontalLayout.addWidget(self.checkBox_save_preview)

        self.horizontalSpacer_2 = QSpacerItem(379, 21, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.graphWidget = ImageView(Widget_Preview)
        self.graphWidget.setObjectName(u"graphWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphWidget.sizePolicy().hasHeightForWidth())
        self.graphWidget.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.graphWidget)


        self.retranslateUi(Widget_Preview)

        QMetaObject.connectSlotsByName(Widget_Preview)
    # setupUi

    def retranslateUi(self, Widget_Preview):
        Widget_Preview.setWindowTitle(QCoreApplication.translate("Widget_Preview", u"Preview", None))
        self.pushButton_detect_lines.setText(QCoreApplication.translate("Widget_Preview", u"\u7ebf\u6bb5\u8bc6\u522b\u9884\u89c8", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Widget_Preview", u"\u4ec5\u6c34\u5e73\u7ebf", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Widget_Preview", u"\u4ec5\u7ad6\u76f4\u7ebf", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Widget_Preview", u"\u6240\u6709\u7ebf\u6bb5", None))

        self.pushButton_clear_lines.setText(QCoreApplication.translate("Widget_Preview", u"\u6e05\u9664\u7ebf\u6bb5", None))
        self.pushButton_update_image.setText(QCoreApplication.translate("Widget_Preview", u"\u66f4\u65b0\u9884\u89c8", None))
        self.pushButton_reverse_image.setText(QCoreApplication.translate("Widget_Preview", u"\u53cd\u8272\u56fe\u50cf", None))
        self.checkBox_save_preview.setText(QCoreApplication.translate("Widget_Preview", u"\u4fdd\u5b58\u9884\u89c8", None))
    # retranslateUi

