# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'locate.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_Dialog_locate(object):
    def setupUi(self, Dialog_locate):
        if not Dialog_locate.objectName():
            Dialog_locate.setObjectName(u"Dialog_locate")
        Dialog_locate.resize(680, 107)
        Dialog_locate.setWindowOpacity(0.700000000000000)
        self.gridLayout = QGridLayout(Dialog_locate)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 1, 0, 1, 1)

        self.pushButton_preview = QPushButton(Dialog_locate)
        self.pushButton_preview.setObjectName(u"pushButton_preview")

        self.gridLayout.addWidget(self.pushButton_preview, 1, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 3, 1, 1)

        self.label = QLabel(Dialog_locate)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 1, 1, 1)

        self.pushButton_locate = QPushButton(Dialog_locate)
        self.pushButton_locate.setObjectName(u"pushButton_locate")

        self.gridLayout.addWidget(self.pushButton_locate, 1, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 3, 2, 1, 1)


        self.retranslateUi(Dialog_locate)

        QMetaObject.connectSlotsByName(Dialog_locate)
    # setupUi

    def retranslateUi(self, Dialog_locate):
        Dialog_locate.setWindowTitle(QCoreApplication.translate("Dialog_locate", u"Locate", None))
        self.pushButton_preview.setText(QCoreApplication.translate("Dialog_locate", u"\u9884\u89c8", None))
        self.label.setText(QCoreApplication.translate("Dialog_locate", u"\u8bf7\u5c06\u6b64\u7a97\u53e3(\u5305\u62ec\u6807\u9898\u680f)\u6070\u597d\u5b8c\u5168\u8986\u76d6\u66f2\u8c31\u4f4d\u7f6e\uff0c\u70b9\u51fb\u6309\u94ae\u66f4\u65b0\u8303\u56f4\u6570\u636e\u3002\n"
"\u968f\u540e\u5173\u95ed\u6216\u79fb\u5f00\u8be5\u7a97\u53e3\uff0c\u786e\u4fdd\u4fdd\u5c4f\u5e55\u66f2\u8c31\u90e8\u5206\u4e0d\u88ab\u906e\u6321\uff0c\u5728\u4e3b\u7a97\u53e3\u8fdb\u884c\u9884\u89c8\u53ca\u4e0b\u4e00\u6b65\u64cd\u4f5c", None))
        self.pushButton_locate.setText(QCoreApplication.translate("Dialog_locate", u"\u5b9a\u4f4d", None))
    # retranslateUi

