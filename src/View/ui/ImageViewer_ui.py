# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ImageViewer.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QSizePolicy, QWidget)

from pyqtgraph import ImageView

class Ui_ImageViewer(object):
    def setupUi(self, ImageViewer):
        if not ImageViewer.objectName():
            ImageViewer.setObjectName(u"ImageViewer")
        ImageViewer.resize(832, 266)
        self.gridLayout = QGridLayout(ImageViewer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.imageView = ImageView(ImageViewer)
        self.imageView.setObjectName(u"imageView")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageView.sizePolicy().hasHeightForWidth())
        self.imageView.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.imageView, 0, 0, 1, 1)


        self.retranslateUi(ImageViewer)

        QMetaObject.connectSlotsByName(ImageViewer)
    # setupUi

    def retranslateUi(self, ImageViewer):
        ImageViewer.setWindowTitle(QCoreApplication.translate("ImageViewer", u"Form", None))
    # retranslateUi

