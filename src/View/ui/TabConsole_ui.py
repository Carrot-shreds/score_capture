# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TabConsole.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QLabel, QLayout, QPushButton, QSizePolicy,
    QSpacerItem, QTextEdit, QVBoxLayout, QWidget)

class Ui_TabConsole(object):
    def setupUi(self, TabConsole):
        if not TabConsole.objectName():
            TabConsole.setObjectName(u"TabConsole")
        TabConsole.resize(877, 0)
        self.verticalLayout = QVBoxLayout(TabConsole)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_settings = QGridLayout()
        self.gridLayout_settings.setObjectName(u"gridLayout_settings")
        self.gridLayout_settings.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_settings.setContentsMargins(10, -1, 10, -1)
        self.horizontalSpacer_center = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_settings.addItem(self.horizontalSpacer_center, 0, 3, 1, 1)

        self.checkBox_auto_scroll = QCheckBox(TabConsole)
        self.checkBox_auto_scroll.setObjectName(u"checkBox_auto_scroll")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_auto_scroll.sizePolicy().hasHeightForWidth())
        self.checkBox_auto_scroll.setSizePolicy(sizePolicy)
        self.checkBox_auto_scroll.setChecked(False)
        self.checkBox_auto_scroll.setTristate(False)

        self.gridLayout_settings.addWidget(self.checkBox_auto_scroll, 0, 4, 1, 1)

        self.pushButton_clear_console = QPushButton(TabConsole)
        self.pushButton_clear_console.setObjectName(u"pushButton_clear_console")
        sizePolicy.setHeightForWidth(self.pushButton_clear_console.sizePolicy().hasHeightForWidth())
        self.pushButton_clear_console.setSizePolicy(sizePolicy)
        self.pushButton_clear_console.setMinimumSize(QSize(0, 0))

        self.gridLayout_settings.addWidget(self.pushButton_clear_console, 0, 5, 1, 1)

        self.horizontalSpacer_left = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_settings.addItem(self.horizontalSpacer_left, 0, 0, 1, 1)

        self.label_log_level = QLabel(TabConsole)
        self.label_log_level.setObjectName(u"label_log_level")
        self.label_log_level.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_settings.addWidget(self.label_log_level, 0, 1, 1, 1)

        self.comboBox_log_level = QComboBox(TabConsole)
        self.comboBox_log_level.addItem("")
        self.comboBox_log_level.addItem("")
        self.comboBox_log_level.addItem("")
        self.comboBox_log_level.addItem("")
        self.comboBox_log_level.addItem("")
        self.comboBox_log_level.setObjectName(u"comboBox_log_level")
        sizePolicy.setHeightForWidth(self.comboBox_log_level.sizePolicy().hasHeightForWidth())
        self.comboBox_log_level.setSizePolicy(sizePolicy)
        self.comboBox_log_level.setMinimumSize(QSize(90, 0))
        self.comboBox_log_level.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        self.gridLayout_settings.addWidget(self.comboBox_log_level, 0, 2, 1, 1)

        self.horizontalSpacer_right = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_settings.addItem(self.horizontalSpacer_right, 0, 6, 1, 1)

        self.gridLayout_settings.setColumnStretch(0, 1)
        self.gridLayout_settings.setColumnStretch(1, 1)
        self.gridLayout_settings.setColumnStretch(2, 1)
        self.gridLayout_settings.setColumnStretch(3, 1)
        self.gridLayout_settings.setColumnStretch(4, 1)
        self.gridLayout_settings.setColumnStretch(5, 1)
        self.gridLayout_settings.setColumnStretch(6, 1)

        self.verticalLayout.addLayout(self.gridLayout_settings)

        self.textEdit_console = QTextEdit(TabConsole)
        self.textEdit_console.setObjectName(u"textEdit_console")

        self.verticalLayout.addWidget(self.textEdit_console)


        self.retranslateUi(TabConsole)

        QMetaObject.connectSlotsByName(TabConsole)
    # setupUi

    def retranslateUi(self, TabConsole):
        TabConsole.setWindowTitle(QCoreApplication.translate("TabConsole", u"Form", None))
        self.checkBox_auto_scroll.setText(QCoreApplication.translate("TabConsole", u"\u81ea\u52a8\u6eda\u52a8", None))
        self.pushButton_clear_console.setText(QCoreApplication.translate("TabConsole", u"\u6e05\u7a7a\u8f93\u51fa", None))
        self.label_log_level.setText(QCoreApplication.translate("TabConsole", u"\u65e5\u5fd7\u7b49\u7ea7\uff1a", None))
        self.comboBox_log_level.setItemText(0, QCoreApplication.translate("TabConsole", u"DEBUG", None))
        self.comboBox_log_level.setItemText(1, QCoreApplication.translate("TabConsole", u"INFO", None))
        self.comboBox_log_level.setItemText(2, QCoreApplication.translate("TabConsole", u"SUCCESS", None))
        self.comboBox_log_level.setItemText(3, QCoreApplication.translate("TabConsole", u"WARNING", None))
        self.comboBox_log_level.setItemText(4, QCoreApplication.translate("TabConsole", u"ERROR", None))

    # retranslateUi

