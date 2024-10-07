# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QLCDNumber, QLabel,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QStatusBar, QTabWidget,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(839, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.lcdTemp = QLCDNumber(self.centralwidget)
        self.lcdTemp.setObjectName(u"lcdTemp")
        self.lcdTemp.setGeometry(QRect(650, 10, 131, 111))
        self.lcdTemp.setStyleSheet(u"color: skyblue")
        self.lcdTemp.setSmallDecimalPoint(False)
        self.lcdTemp.setMode(QLCDNumber.Mode.Oct)
        self.lcdTemp.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        self.TempLabel = QLabel(self.centralwidget)
        self.TempLabel.setObjectName(u"TempLabel")
        self.TempLabel.setGeometry(QRect(650, 130, 141, 20))
        self.TempLabel.setStyleSheet(u"font: ")
        self.TempProgessBar = QProgressBar(self.centralwidget)
        self.TempProgessBar.setObjectName(u"TempProgessBar")
        self.TempProgessBar.setGeometry(QRect(790, 10, 31, 111))
        self.TempProgessBar.setValue(24)
        self.TempProgessBar.setOrientation(Qt.Orientation.Vertical)
        self.lcdLuft = QLCDNumber(self.centralwidget)
        self.lcdLuft.setObjectName(u"lcdLuft")
        self.lcdLuft.setGeometry(QRect(650, 190, 131, 111))
        self.lcdLuft.setStyleSheet(u"color: skyblue")
        self.lcdLuft.setSmallDecimalPoint(False)
        self.lcdLuft.setMode(QLCDNumber.Mode.Oct)
        self.lcdLuft.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        self.LuftLabel = QLabel(self.centralwidget)
        self.LuftLabel.setObjectName(u"LuftLabel")
        self.LuftLabel.setGeometry(QRect(650, 310, 141, 16))
        self.lcdGesamtzahl = QLCDNumber(self.centralwidget)
        self.lcdGesamtzahl.setObjectName(u"lcdGesamtzahl")
        self.lcdGesamtzahl.setGeometry(QRect(650, 360, 131, 111))
        self.lcdGesamtzahl.setStyleSheet(u"color: skyblue")
        self.lcdGesamtzahl.setSmallDecimalPoint(False)
        self.lcdGesamtzahl.setMode(QLCDNumber.Mode.Oct)
        self.lcdGesamtzahl.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(650, 480, 131, 16))
        self.plotButton = QPushButton(self.centralwidget)
        self.plotButton.setObjectName(u"plotButton")
        self.plotButton.setGeometry(QRect(654, 510, 111, 24))
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 641, 551))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.graphicsView = QGraphicsView(self.tab)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(0, 0, 641, 531))
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.graphicsView_2 = QGraphicsView(self.tab_2)
        self.graphicsView_2.setObjectName(u"graphicsView_2")
        self.graphicsView_2.setGeometry(QRect(-5, -9, 641, 541))
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 839, 22))
        self.menuDatei = QMenu(self.menubar)
        self.menuDatei.setObjectName(u"menuDatei")
        self.menuAnsicht = QMenu(self.menubar)
        self.menuAnsicht.setObjectName(u"menuAnsicht")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuDatei.menuAction())
        self.menubar.addAction(self.menuAnsicht.menuAction())

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.TempLabel.setText(QCoreApplication.translate("MainWindow", u"Temperature in \u00b0C", None))
        self.LuftLabel.setText(QCoreApplication.translate("MainWindow", u"Luftfeuchgtigkeit in %", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Anzahl der Flederm\u00e4use", None))
        self.plotButton.setText(QCoreApplication.translate("MainWindow", u"Plot Data", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.menuDatei.setTitle(QCoreApplication.translate("MainWindow", u"Datei", None))
        self.menuAnsicht.setTitle(QCoreApplication.translate("MainWindow", u"Ansicht", None))
    # retranslateUi

