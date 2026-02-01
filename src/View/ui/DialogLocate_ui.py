# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DialogLocate.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QWidget)

class Ui_DialogLocate(object):
    def setupUi(self, DialogLocate):
        if not DialogLocate.objectName():
            DialogLocate.setObjectName(u"DialogLocate")
        DialogLocate.resize(844, 186)
        DialogLocate.setWindowOpacity(0.700000000000000)
        self.gridLayout = QGridLayout(DialogLocate)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(DialogLocate)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(self.widget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.spinBox_region_height = QSpinBox(self.frame)
        self.spinBox_region_height.setObjectName(u"spinBox_region_height")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.spinBox_region_height.sizePolicy().hasHeightForWidth())
        self.spinBox_region_height.setSizePolicy(sizePolicy1)
        self.spinBox_region_height.setMinimumSize(QSize(80, 0))
        self.spinBox_region_height.setMaximum(2000)

        self.gridLayout_2.addWidget(self.spinBox_region_height, 0, 9, 1, 1)

        self.pushButton_preview = QPushButton(self.frame)
        self.pushButton_preview.setObjectName(u"pushButton_preview")

        self.gridLayout_2.addWidget(self.pushButton_preview, 1, 3, 1, 1)

        self.checkBox_dialog_always_on_top = QCheckBox(self.frame)
        self.checkBox_dialog_always_on_top.setObjectName(u"checkBox_dialog_always_on_top")

        self.gridLayout_2.addWidget(self.checkBox_dialog_always_on_top, 1, 5, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(85, 25, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 0, 10, 1, 3)

        self.checkBox_live_locate = QCheckBox(self.frame)
        self.checkBox_live_locate.setObjectName(u"checkBox_live_locate")

        self.gridLayout_2.addWidget(self.checkBox_live_locate, 1, 6, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(86, 25, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 1, 12, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(101, 25, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 1, 0, 1, 2)

        self.label_8 = QLabel(self.frame)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMouseTracking(False)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_8, 0, 8, 1, 1)

        self.pushButton_close = QPushButton(self.frame)
        self.pushButton_close.setObjectName(u"pushButton_close")

        self.gridLayout_2.addWidget(self.pushButton_close, 1, 9, 1, 1)

        self.pushButton_locate = QPushButton(self.frame)
        self.pushButton_locate.setObjectName(u"pushButton_locate")

        self.gridLayout_2.addWidget(self.pushButton_locate, 1, 2, 1, 1)

        self.pushButton_minimize = QPushButton(self.frame)
        self.pushButton_minimize.setObjectName(u"pushButton_minimize")

        self.gridLayout_2.addWidget(self.pushButton_minimize, 1, 8, 1, 1)

        self.checkBox_reverse_image = QCheckBox(self.frame)
        self.checkBox_reverse_image.setObjectName(u"checkBox_reverse_image")

        self.gridLayout_2.addWidget(self.checkBox_reverse_image, 1, 4, 1, 1)

        self.spinBox_region_width = QSpinBox(self.frame)
        self.spinBox_region_width.setObjectName(u"spinBox_region_width")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.spinBox_region_width.sizePolicy().hasHeightForWidth())
        self.spinBox_region_width.setSizePolicy(sizePolicy2)
        self.spinBox_region_width.setMinimumSize(QSize(80, 0))
        self.spinBox_region_width.setMaximum(2000)

        self.gridLayout_2.addWidget(self.spinBox_region_width, 0, 7, 1, 1)

        self.label_7 = QLabel(self.frame)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMouseTracking(False)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_7, 0, 6, 1, 1)

        self.spinBox_region_y = QSpinBox(self.frame)
        self.spinBox_region_y.setObjectName(u"spinBox_region_y")
        sizePolicy2.setHeightForWidth(self.spinBox_region_y.sizePolicy().hasHeightForWidth())
        self.spinBox_region_y.setSizePolicy(sizePolicy2)
        self.spinBox_region_y.setMinimumSize(QSize(80, 0))
        self.spinBox_region_y.setMaximum(2000)

        self.gridLayout_2.addWidget(self.spinBox_region_y, 0, 5, 1, 1)

        self.label_11 = QLabel(self.frame)
        self.label_11.setObjectName(u"label_11")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy3)
        self.label_11.setMouseTracking(False)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_11, 0, 4, 1, 1)

        self.spinBox_region_x = QSpinBox(self.frame)
        self.spinBox_region_x.setObjectName(u"spinBox_region_x")
        sizePolicy2.setHeightForWidth(self.spinBox_region_x.sizePolicy().hasHeightForWidth())
        self.spinBox_region_x.setSizePolicy(sizePolicy2)
        self.spinBox_region_x.setMinimumSize(QSize(80, 0))
        self.spinBox_region_x.setMaximum(2000)

        self.gridLayout_2.addWidget(self.spinBox_region_x, 0, 3, 1, 1)

        self.label_9 = QLabel(self.frame)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMouseTracking(False)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_9, 0, 2, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(96, 25, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_6, 0, 0, 1, 2)


        self.horizontalLayout.addWidget(self.frame)


        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)


        self.retranslateUi(DialogLocate)

        QMetaObject.connectSlotsByName(DialogLocate)
    # setupUi

    def retranslateUi(self, DialogLocate):
        DialogLocate.setWindowTitle(QCoreApplication.translate("DialogLocate", u"Locate", None))
        self.pushButton_preview.setText(QCoreApplication.translate("DialogLocate", u"\u9884\u89c8", None))
        self.checkBox_dialog_always_on_top.setText(QCoreApplication.translate("DialogLocate", u"\u7a97\u53e3\u7f6e\u9876", None))
        self.checkBox_live_locate.setText(QCoreApplication.translate("DialogLocate", u"\u5b9e\u65f6\u66f4\u65b0", None))
        self.label_8.setText(QCoreApplication.translate("DialogLocate", u"\u9ad8:", None))
        self.pushButton_close.setText(QCoreApplication.translate("DialogLocate", u"\u5173\u95ed", None))
        self.pushButton_locate.setText(QCoreApplication.translate("DialogLocate", u"\u5b9a\u4f4d", None))
        self.pushButton_minimize.setText(QCoreApplication.translate("DialogLocate", u"\u6700\u5c0f\u5316", None))
        self.checkBox_reverse_image.setText(QCoreApplication.translate("DialogLocate", u"\u56fe\u7247\u53cd\u76f8", None))
        self.label_7.setText(QCoreApplication.translate("DialogLocate", u"\u5bbd:", None))
        self.label_11.setText(QCoreApplication.translate("DialogLocate", u"Y:", None))
        self.label_9.setText(QCoreApplication.translate("DialogLocate", u"X:", None))
    # retranslateUi

