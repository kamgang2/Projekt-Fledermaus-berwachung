# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QMainWindow, QMenuBar,
    QSizePolicy, QStatusBar, QWidget, QVBoxLayout, QPushButton, QLCDNumber, QGridLayout, QLabel, QProgressBar)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800,600)
       

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.layout = QGridLayout(self.centralwidget)

        self.graphicsView = QGraphicsView()
        self.graphicsView.setObjectName(u"graphicsView")
        self.layout.addWidget(self.graphicsView, 0, 0, 10, 10)

        self.lcdTemp = QLCDNumber()
        self.lcdTemp.setObjectName(u"lcdTemp")
        self.lcdTemp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.lcdTemp, 0, 11, 2, 2)
        lcdTempHeight = getHight(self.lcdTemp)
        
        # self.TempProgressBar = QProgressBar()
        # self.TempProgressBar.setObjectName(u"TempProgessBar")
        # self.TempProgressBar.setOrientation(Qt.Vertical)
        # self.TempProgressBar.setMaximumHeight(20)
        # self.layout.addWidget(self.TempProgressBar,0,14)

        self.TempLabel = QLabel("Temperature in °C")
        self.TempLabel.setObjectName(u"TempLabel")
        self.layout.addWidget(self.TempLabel, 2,11, 1, 2)

        self.lcdLuft = QLCDNumber()
        self.lcdLuft.setObjectName(u"lcdLuft")
        self.layout.addWidget(self.lcdLuft,3,11,2,2)

        self.LuftLabel = QLabel("Luftfeuchtigkeit in %")
        self.TempLabel.setObjectName(u"LuftLabel")
        self.layout.addWidget(self.LuftLabel, 5,11, 1, 2)

        self.lcdGesamtzahl = QLCDNumber()
        self.lcdGesamtzahl.setObjectName(u"lcdGesamtzahl")
        self.layout.addWidget(self.lcdGesamtzahl, 8,11, 2, 2)  


        self.plotButton = QPushButton("Plot Data", self.centralwidget)
        self.plotButton.setObjectName(u"plotButton")
        self.layout.addWidget(self.plotButton)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
    
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
 

   
def getHight(element):
    return element.height()
