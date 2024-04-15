# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
    QPlainTextEdit, QPushButton, QSizePolicy, QWidget)
import images_rc

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        if not AboutDialog.objectName():
            AboutDialog.setObjectName(u"AboutDialog")
        AboutDialog.resize(450, 350)
        font = QFont()
        font.setPointSize(13)
        AboutDialog.setFont(font)
        self.gridLayout_2 = QGridLayout(AboutDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(AboutDialog)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setPixmap(QPixmap(u":/img/imgs/information.png"))
        self.label.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.le_info = QPlainTextEdit(AboutDialog)
        self.le_info.setObjectName(u"le_info")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(4)
        sizePolicy1.setVerticalStretch(4)
        sizePolicy1.setHeightForWidth(self.le_info.sizePolicy().hasHeightForWidth())
        self.le_info.setSizePolicy(sizePolicy1)
        self.le_info.setFocusPolicy(Qt.ClickFocus)
        self.le_info.setReadOnly(True)

        self.gridLayout.addWidget(self.le_info, 1, 1, 1, 2)

        self.pbtn_ok = QPushButton(AboutDialog)
        self.pbtn_ok.setObjectName(u"pbtn_ok")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.pbtn_ok.sizePolicy().hasHeightForWidth())
        self.pbtn_ok.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.pbtn_ok, 2, 2, 1, 1)

        self.label_2 = QLabel(AboutDialog)
        self.label_2.setObjectName(u"label_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 2)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(AboutDialog)
        self.pbtn_ok.clicked.connect(AboutDialog.close)

        QMetaObject.connectSlotsByName(AboutDialog)
    # setupUi

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QCoreApplication.translate("AboutDialog", u"\u5173\u4e8e", None))
        self.label.setText("")
        self.le_info.setPlainText(QCoreApplication.translate("AboutDialog", u"\u672c\u7a0b\u5e8f\u662f\u6839\u636e\u300a\u8ba1\u7b97\u673a\u7cfb\u7edf\u8981\u7d20\uff1a\u4ece\u96f6\u5f00\u59cb\u6784\u5efa\u73b0\u4ee3\u8ba1\u7b97\u673a\u300b\u4e00\u4e66\u7b2c\u516d\u7ae0\u8981\u6c42\uff0c\u7f16\u5199\u7684\u7f16\u8bd1\u5668\u6837\u4f8b\u3002\n"
"\n"
"\u7248\u672c\uff1a1.0\n"
"\u8d21\u732e\u8005\uff1a\u4f5b\u5929\u9b54\u97f3\n"
"Python\uff1a3.10\n"
"Pyside6\uff1a6.6.1", None))
        self.le_info.setProperty("html", "")
        self.le_info.setProperty("text", "")
        self.pbtn_ok.setText(QCoreApplication.translate("AboutDialog", u"\u786e\u5b9a", None))
        self.label_2.setText(QCoreApplication.translate("AboutDialog", u"\u7f16\u8bd1\u5668", None))
    # retranslateUi

