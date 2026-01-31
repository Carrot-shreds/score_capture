# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SideBar.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_SideBar(object):
    def setupUi(self, SideBar):
        if not SideBar.objectName():
            SideBar.setObjectName(u"SideBar")
        SideBar.resize(168, 0)
        self.verticalLayout = QVBoxLayout(SideBar)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_logo = QLabel(SideBar)
        self.label_logo.setObjectName(u"label_logo")
        font = QFont()
        font.setPointSize(22)
        self.label_logo.setFont(font)
        self.label_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_logo.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_logo)

        self.pushButton_locate = QPushButton(SideBar)
        self.pushButton_locate.setObjectName(u"pushButton_locate")

        self.verticalLayout.addWidget(self.pushButton_locate)

        self.pushButton_preview = QPushButton(SideBar)
        self.pushButton_preview.setObjectName(u"pushButton_preview")

        self.verticalLayout.addWidget(self.pushButton_preview)

        self.pushButton_capture = QPushButton(SideBar)
        self.pushButton_capture.setObjectName(u"pushButton_capture")

        self.verticalLayout.addWidget(self.pushButton_capture)

        self.pushButton_stitch = QPushButton(SideBar)
        self.pushButton_stitch.setObjectName(u"pushButton_stitch")

        self.verticalLayout.addWidget(self.pushButton_stitch)

        self.pushButton_reclip = QPushButton(SideBar)
        self.pushButton_reclip.setObjectName(u"pushButton_reclip")

        self.verticalLayout.addWidget(self.pushButton_reclip)

        self.verticalSpacer = QSpacerItem(20, 33, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.pushButton_instruction = QPushButton(SideBar)
        self.pushButton_instruction.setObjectName(u"pushButton_instruction")

        self.verticalLayout.addWidget(self.pushButton_instruction)

        self.gridLayout_bottom = QGridLayout()
        self.gridLayout_bottom.setObjectName(u"gridLayout_bottom")
        self.label_repo = QLabel(SideBar)
        self.label_repo.setObjectName(u"label_repo")
        self.label_repo.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.label_repo.setWordWrap(False)
        self.label_repo.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout_bottom.addWidget(self.label_repo, 0, 0, 1, 1)

        self.label_version = QLabel(SideBar)
        self.label_version.setObjectName(u"label_version")
        self.label_version.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_version.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout_bottom.addWidget(self.label_version, 0, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_bottom)


        self.retranslateUi(SideBar)

        QMetaObject.connectSlotsByName(SideBar)
    # setupUi

    def retranslateUi(self, SideBar):
        SideBar.setWindowTitle(QCoreApplication.translate("SideBar", u"Form", None))
        self.label_logo.setText(QCoreApplication.translate("SideBar", u"Score Capture", None))
        self.pushButton_locate.setText(QCoreApplication.translate("SideBar", u"\u5b9a\u4f4d", None))
        self.pushButton_preview.setText(QCoreApplication.translate("SideBar", u"\u9884\u89c8", None))
        self.pushButton_capture.setText(QCoreApplication.translate("SideBar", u"\u5f00\u59cb\u622a\u56fe", None))
        self.pushButton_stitch.setText(QCoreApplication.translate("SideBar", u"\u62fc\u63a5", None))
        self.pushButton_reclip.setText(QCoreApplication.translate("SideBar", u"\u91cd\u5206\u5272", None))
        self.pushButton_instruction.setText(QCoreApplication.translate("SideBar", u"\u6253\u5f00\u8bf4\u660e\u6587\u6863", None))
        self.label_repo.setText(QCoreApplication.translate("SideBar", u"<a href='https://github.com/Carrot-shreds/score_capture'>Github repo</a>", None))
        self.label_version.setText(QCoreApplication.translate("SideBar", u"V0.0.0", None))
    # retranslateUi

