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
    QPushButton, QSizePolicy, QStatusBar, QWidget, QGridLayout)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(839, 600)
        
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        # Layout für das zentrale Widget
        self.gridLayout = QGridLayout(self.centralwidget)
        
        # Grafikansicht
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 17, 1)
        
        # Temperatur LCD
        self.lcdTemp = QLCDNumber(self.centralwidget)
        self.lcdTemp.setObjectName(u"lcdTemp")
        self.lcdTemp.setStyleSheet(u"color: skyblue")
        self.lcdTemp.setSmallDecimalPoint(False)
        self.lcdTemp.setMode(QLCDNumber.Mode.Dec)
        self.lcdTemp.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        self.gridLayout.addWidget(self.lcdTemp, 0, 1, 3,1)

        # Temperatur Label
        self.TempLabel = QLabel(self.centralwidget)
        self.TempLabel.setObjectName(u"TempLabel")
        self.TempLabel.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.TempLabel, 3, 1)

        # Temperatur Fortschrittsbalken
        self.TempProgessBar = QProgressBar(self.centralwidget)
        self.TempProgessBar.setObjectName(u"TempProgessBar")
        self.TempProgessBar.setRange(-20, 50)
        self.TempProgessBar.setOrientation(Qt.Vertical)
        self.gridLayout.addWidget(self.TempProgessBar, 0, 2, 3, 1)

        # Luftfeuchtigkeit LCD
        self.lcdLuft = QLCDNumber(self.centralwidget)
        self.lcdLuft.setObjectName(u"lcdLuft")
        self.lcdLuft.setStyleSheet(u"color: skyblue")
        self.lcdLuft.setSmallDecimalPoint(False)
        self.lcdLuft.setMode(QLCDNumber.Mode.Dec)
        self.lcdLuft.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        self.gridLayout.addWidget(self.lcdLuft, 6, 1,3,1)

        # Luftfeuchtigkeit Label
        self.LuftLabel = QLabel(self.centralwidget)
        self.LuftLabel.setObjectName(u"LuftLabel")
        self.LuftLabel.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.LuftLabel, 9, 1)

        # Gesamtzahl LCD
        self.lcdGesamtzahl = QLCDNumber(self.centralwidget)
        self.lcdGesamtzahl.setObjectName(u"lcdGesamtzahl")
        self.lcdGesamtzahl.setStyleSheet(u"color: skyblue")
        self.lcdGesamtzahl.setSmallDecimalPoint(False)
        self.lcdGesamtzahl.setMode(QLCDNumber.Mode.Dec)
        self.lcdGesamtzahl.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        self.gridLayout.addWidget(self.lcdGesamtzahl, 12, 1,3,1)

        # Gesamtzahl Label
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label, 15, 1)

        # Plot Button
        self.plotButton = QPushButton(self.centralwidget)
        self.plotButton.setObjectName(u"plotButton")
        self.gridLayout.addWidget(self.plotButton, 16, 1, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        MainWindow.setMenuBar(self.menubar)
        self.menuDatei = QMenu(self.menubar)

        self.menuDatei.setObjectName(u"menuDatei")
        self.menuDatei.addAction("als Excel exportieren")
        self.menuAnsicht = QMenu(self.menubar)

        self.menuAnsicht.setObjectName(u"menuAnsicht")
        self.menuAnsicht.addAction("Tag")
        self.menuAnsicht.addAction("Wochen")
        self.menuAnsicht.addAction("Monat")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuDatei.menuAction())
        self.menubar.addAction(self.menuAnsicht.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.TempLabel.setText(QCoreApplication.translate("MainWindow", u"Temperature in \u00b0C", None))
        self.LuftLabel.setText(QCoreApplication.translate("MainWindow", u"Luftfeuchtigkeit in %", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Anzahl der Fledermäuse", None))
        self.plotButton.setText(QCoreApplication.translate("MainWindow", u"Plot Data", None))
        self.menuDatei.setTitle(QCoreApplication.translate("MainWindow", u"Datei", None))
        self.menuAnsicht.setTitle(QCoreApplication.translate("MainWindow", u"Ansicht", None))

