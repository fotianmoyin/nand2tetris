# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QToolBar, QWidget)
import images_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1024, 700)
        font = QFont()
        font.setPointSize(13)
        MainWindow.setFont(font)
        self.action_load_source_file = QAction(MainWindow)
        self.action_load_source_file.setObjectName(u"action_load_source_file")
        icon = QIcon()
        icon.addFile(u":/img/imgs/opendoc.gif", QSize(), QIcon.Normal, QIcon.Off)
        self.action_load_source_file.setIcon(icon)
        self.action_save_destination_file = QAction(MainWindow)
        self.action_save_destination_file.setObjectName(u"action_save_destination_file")
        icon1 = QIcon()
        icon1.addFile(u":/img/imgs/save.gif", QSize(), QIcon.Normal, QIcon.Off)
        self.action_save_destination_file.setIcon(icon1)
        self.action_load_comparison_file = QAction(MainWindow)
        self.action_load_comparison_file.setObjectName(u"action_load_comparison_file")
        icon2 = QIcon()
        icon2.addFile(u":/img/imgs/smallequal.gif", QSize(), QIcon.Normal, QIcon.Off)
        self.action_load_comparison_file.setIcon(icon2)
        self.action_exit = QAction(MainWindow)
        self.action_exit.setObjectName(u"action_exit")
        self.action_single_step = QAction(MainWindow)
        self.action_single_step.setObjectName(u"action_single_step")
        icon3 = QIcon()
        icon3.addFile(u":/img/imgs/vcrforward.gif", QSize(), QIcon.Normal, QIcon.Off)
        self.action_single_step.setIcon(icon3)
        self.action_fast_forward = QAction(MainWindow)
        self.action_fast_forward.setObjectName(u"action_fast_forward")
        icon4 = QIcon()
        icon4.addFile(u":/img/imgs/vcrfastforward.gif", QSize(), QIcon.Normal, QIcon.Off)
        self.action_fast_forward.setIcon(icon4)
        self.action_stop = QAction(MainWindow)
        self.action_stop.setObjectName(u"action_stop")
        icon5 = QIcon()
        icon5.addFile(u":/img/imgs/vcrstop.gif", QSize(), QIcon.Normal, QIcon.Off)
        self.action_stop.setIcon(icon5)
        self.action_fast_translation = QAction(MainWindow)
        self.action_fast_translation.setObjectName(u"action_fast_translation")
        icon6 = QIcon()
        icon6.addFile(u":/img/imgs/hex.gif", QSize(), QIcon.Normal, QIcon.Off)
        self.action_fast_translation.setIcon(icon6)
        self.action_help = QAction(MainWindow)
        self.action_help.setObjectName(u"action_help")
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.action_rewind = QAction(MainWindow)
        self.action_rewind.setObjectName(u"action_rewind")
        icon7 = QIcon()
        icon7.addFile(u":/img/imgs/vcrrewind.gif", QSize(), QIcon.Normal, QIcon.Off)
        self.action_rewind.setIcon(icon7)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_4 = QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setPixmap(QPixmap(u":/img/imgs/arrow2.gif"))

        self.gridLayout_4.addWidget(self.label_4, 0, 1, 1, 1)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setPixmap(QPixmap(u":/img/imgs/equal.gif"))

        self.gridLayout_4.addWidget(self.label_5, 0, 3, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMargin(5)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lsw_asm = QListWidget(self.centralwidget)
        self.lsw_asm.setObjectName(u"lsw_asm")
        self.lsw_asm.setUniformItemSizes(False)
        self.lsw_asm.setSelectionRectVisible(False)

        self.gridLayout.addWidget(self.lsw_asm, 1, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMargin(5)

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.lsw_hack = QListWidget(self.centralwidget)
        self.lsw_hack.setObjectName(u"lsw_hack")

        self.gridLayout_2.addWidget(self.lsw_hack, 1, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 2, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMargin(5)

        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)

        self.lsw_compare = QListWidget(self.centralwidget)
        self.lsw_compare.setObjectName(u"lsw_compare")

        self.gridLayout_3.addWidget(self.lsw_compare, 1, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 4, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1024, 30))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_file.setFont(font)
        self.menu_run = QMenu(self.menubar)
        self.menu_run.setObjectName(u"menu_run")
        self.menu_run.setFont(font)
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName(u"menu_help")
        self.menu_help.setFont(font)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(True)
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setIconSize(QSize(32, 32))
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_run.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.action_load_source_file)
        self.menu_file.addAction(self.action_save_destination_file)
        self.menu_file.addAction(self.action_load_comparison_file)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)
        self.menu_run.addAction(self.action_single_step)
        self.menu_run.addAction(self.action_fast_forward)
        self.menu_run.addAction(self.action_stop)
        self.menu_run.addAction(self.action_rewind)
        self.menu_run.addSeparator()
        self.menu_run.addAction(self.action_fast_translation)
        self.menu_help.addAction(self.action_help)
        self.menu_help.addAction(self.action_about)
        self.toolBar.addAction(self.action_load_source_file)
        self.toolBar.addAction(self.action_save_destination_file)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_single_step)
        self.toolBar.addAction(self.action_fast_forward)
        self.toolBar.addAction(self.action_stop)
        self.toolBar.addAction(self.action_rewind)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_fast_translation)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_load_comparison_file)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u6c47\u7f16\u7f16\u8bd1\u5668", None))
        self.action_load_source_file.setText(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u6c47\u7f16\u7a0b\u5e8f", None))
#if QT_CONFIG(tooltip)
        self.action_load_source_file.setToolTip(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u6c47\u7f16\u7a0b\u5e8f", None))
#endif // QT_CONFIG(tooltip)
        self.action_save_destination_file.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u673a\u5668\u4ee3\u7801", None))
#if QT_CONFIG(tooltip)
        self.action_save_destination_file.setToolTip(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u673a\u5668\u4ee3\u7801", None))
#endif // QT_CONFIG(tooltip)
        self.action_load_comparison_file.setText(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u6bd4\u8f83\u4ee3\u7801", None))
#if QT_CONFIG(tooltip)
        self.action_load_comparison_file.setToolTip(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u6bd4\u8f83\u4ee3\u7801", None))
#endif // QT_CONFIG(tooltip)
        self.action_exit.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa", None))
#if QT_CONFIG(shortcut)
        self.action_exit.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+X", None))
#endif // QT_CONFIG(shortcut)
        self.action_single_step.setText(QCoreApplication.translate("MainWindow", u"\u5355\u6b65\u6267\u884c", None))
        self.action_fast_forward.setText(QCoreApplication.translate("MainWindow", u"\u5feb\u901f\u524d\u8fdb", None))
#if QT_CONFIG(tooltip)
        self.action_fast_forward.setToolTip(QCoreApplication.translate("MainWindow", u"\u5feb\u901f\u524d\u8fdb", None))
#endif // QT_CONFIG(tooltip)
        self.action_stop.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62", None))
        self.action_fast_translation.setText(QCoreApplication.translate("MainWindow", u"\u5feb\u901f\u7f16\u8bd1", None))
        self.action_help.setText(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9\u63d0\u793a", None))
#if QT_CONFIG(shortcut)
        self.action_help.setShortcut(QCoreApplication.translate("MainWindow", u"F1", None))
#endif // QT_CONFIG(shortcut)
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.action_rewind.setText(QCoreApplication.translate("MainWindow", u"\u8fd4\u56de\u9996\u884c", None))
        self.label_4.setText("")
        self.label_5.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u6c47\u7f16\u7a0b\u5e8f", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u673a\u5668\u4ee3\u7801", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u6bd4\u8f83\u4ee3\u7801", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
        self.menu_run.setTitle(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

