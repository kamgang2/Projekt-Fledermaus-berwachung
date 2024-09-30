# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QPropertyAnimation, 
    QSize, QTime, QUrl, Qt, QFile, QTextStream)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient, 
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QLCDNumber, QLabel, QGraphicsDropShadowEffect,
    QMainWindow, QMenu, QMenuBar, QProgressBar, QSpinBox,QTabWidget,QVBoxLayout,
    QPushButton, QSizePolicy, QStatusBar, QWidget, QGridLayout, QScrollArea)
import pyqtgraph as pg

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(839, 600)
    
  
      # Lade das Stylesheet aus einer Datei
        file = QFile("style.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            MainWindow.setStyleSheet(stylesheet)
            file.close()

        """Couleurs utilisées : Bleu clair (#E9F1FA), bleu vif (#00ABE4), blanc (#FFFFFF)"""
        # Set background color of the main window
        #MainWindow.setStyleSheet("background-color: #E9F1FA;")  # Change this color as needed

        
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        # Layout für das zentrale Widget
        self.gridLayout = QGridLayout(self.centralwidget)

        # Tabs
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        
        self.tab1 = QWidget()
        self.tab1.setObjectName(u"tab1")
        self.tab1Layout = QVBoxLayout(self.tab1)  # Layout für tab1
        self.plotWidget1 = pg.PlotWidget(self.tab1)
        self.plotWidget1.setLabel('left', 'WERTE', **{'font-size': '14pt', 'font-family': 'arial'})
        self.plotWidget1.setLabel('bottom', 'Zeit', **{'font-size': '14pt', 'font-family': 'Arial'})
        self.plotWidget1.setTitle('Ein- und Aus-Fluege über die Zeit')
         # Schriftart für Titel anpassen
        title_font = QFont('Arial', 14)  # 'Arial' ist die Schriftart, 14pt ist die Schriftgröße
        self.plotWidget1.getPlotItem().setTitle('Ein- und Aus-Fluege über die Zeit', color='black', size='14pt', font=title_font)
        
        # self.label1 = pg.LabelItem(justify='left')
        # self.plotWidget1.addItem(self.label1)
        

        self.plotWidget1.setObjectName(u"plotWidget1")
        self.tab1Layout.addWidget(self.plotWidget1)
        self.tabWidget.addTab(self.tab1, "Fledermausaktivität")
        
        
        self.tab2 = QWidget()
        self.tab2.setObjectName(u"tab2")
        self.tab2Layout = QVBoxLayout(self.tab2)
        self.plotWidget2 = pg.PlotWidget(self.tab2)
        self.viewBox = pg.ViewBox()
        self.plotWidget2.scene().addItem(self.viewBox)
        self.plotWidget2.setLabel('left', 'TEMPERATUR in °C', **{'font-size': '14pt', 'font-family': 'Arial', 'color': 'red'})
        self.plotWidget2.setLabel('bottom', 'Zeit', **{'font-size': '14pt', 'font-family': 'Arial'})
        self.plotWidget2.getAxis('right').setLabel('LUFTFEUCHTIGKEIT in %', **{'font-size': '14pt', 'font-family': 'Arial', 'color': 'blue'})
        self.plotWidget2.setObjectName(u"plotWidget2")
        self.tab2Layout.addWidget(self.plotWidget2)
        self.tabWidget.addTab(self.tab2, "Umweltmessungen")

       
        
      
       

        
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 17, 1)
        
        # Create and set the drop shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(14)
        shadow.setXOffset(5)
        shadow.setYOffset(5)
        shadow.setColor(QColor(20, 35,222))
        
        
        # Temperatur LCD
        self.lcdTemp = QLCDNumber(self.centralwidget)
        self.lcdTemp.setObjectName(u"lcdTemp")
        self.lcdTemp.setStyleSheet(u"color: black")
        self.lcdTemp.setSmallDecimalPoint(False)
        self.lcdTemp.setMode(QLCDNumber.Mode.Dec)
        self.lcdTemp.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        
       
        self.lcdTemp.setGraphicsEffect(shadow)
        self.gridLayout.addWidget(self.lcdTemp, 0, 1, 3,1)

        # Temperatur Label
        self.TempLabel = QLabel(self.centralwidget)
        self.TempLabel.setObjectName(u"TempLabel")
       # self.TempLabel.setFont(Arialont)
        self.TempLabel.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.TempLabel, 3, 1)

        

        # Luftfeuchtigkeit LCD
        self.lcdLuft = QLCDNumber(self.centralwidget)
        self.lcdLuft.setObjectName(u"lcdLuft")
        self.lcdLuft.setStyleSheet(u"color: black")
        self.lcdLuft.setSmallDecimalPoint(False)
        self.lcdLuft.setMode(QLCDNumber.Mode.Dec)
        self.lcdLuft.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        self.gridLayout.addWidget(self.lcdLuft, 6, 1,3,1)

        # Luftfeuchtigkeit Label
        self.LuftLabel = QLabel(self.centralwidget)
        self.LuftLabel.setObjectName(u"LuftLabel")
        self.LuftLabel.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.LuftLabel, 9, 1)

        # Luftfeuchtigkeit Fortschrittsbalken
        self.LuftProgessBar = QProgressBar(self.centralwidget)
        self.LuftProgessBar.setObjectName(u"LuftProgessBar")
        self.LuftProgessBar.setTextVisible(True)
        self.LuftProgessBar.setRange(0, 100)
        self.LuftProgessBar.setOrientation(Qt.Vertical)
        self.gridLayout.addWidget(self.LuftProgessBar, 6, 2, 3, 1)

        # Gesamtzahl LCD
        self.lcdGesamtzahl = QLCDNumber(self.centralwidget)
        self.lcdGesamtzahl.setObjectName(u"lcdGesamtzahl")
        self.lcdGesamtzahl.setStyleSheet(u"color: black")
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
         
        #Menu 
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        MainWindow.setMenuBar(self.menubar)
        self.menuDatei = QMenu(u"Datei",self.menubar)
        #self.menuDatei.setIcon(QIcon("icons/menu-burger.png"))

        self.menuDatei.setObjectName( u"menuDatei")
        self.actionExportExcel = QAction(QIcon("icons/file-xls.png"), u"als Excel exportieren", MainWindow)
        self.menuDatei.addAction(self.actionExportExcel)
        self.actionDateiLoeschen = QAction("Daten Loeschen")
        self.menuDatei.addAction(self.actionDateiLoeschen)

        self.menuAnsicht = QMenu(self.menubar)
        self.menuAnsicht.setObjectName(u"menuAnsicht")
        self.actionTag = QAction("Tag", MainWindow)
        self.actionNormal = QAction("Stunden", MainWindow)
        self.actionMonat = QAction("Monat", MainWindow)
        self.menuAnsicht.addAction(self.actionNormal)
        self.menuAnsicht.addAction(self.actionTag)
        # self.menuAnsicht.addAction(self.actionWochen)
        self.menuAnsicht.addAction(self.actionMonat)

        self.menuEinstellung = QMenu(u"Eintsellung")
        self.actionSetAnzFledermause = QAction(QIcon("icons/settings.png"), "Set Anz der Fledermause", MainWindow)
        self.menuEinstellung.addAction(self.actionSetAnzFledermause)
     

        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuDatei.menuAction())
        self.menubar.addAction(self.menuAnsicht.menuAction())
        self.menubar.addAction(self.menuEinstellung.menuAction())

        # Füge ein leeres QMenu hinzu, um Abstand zu erzeugen
        #spacer_menu = QMenu("                              ", self.menubar)  # Leeres Menü ohne Titel
        #spacer_menu.setObjectName("spacer")
        #self.menubar.addMenu(spacer_menu)

        self.toggle_sidebar_action = QAction("Einzelne Temperature")
        self.menubar.addAction(self.toggle_sidebar_action)



        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
       # MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.TempLabel.setText(QCoreApplication.translate("MainWindow", u"Temperature in \u00b0C", None))
        self.LuftLabel.setText(QCoreApplication.translate("MainWindow", u"Luftfeuchtigkeit in %", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Anzahl der Fledermäuse", None))
        self.plotButton.setText(QCoreApplication.translate("MainWindow", u"Aktualisieren", None))
        self.menuDatei.setTitle(QCoreApplication.translate("MainWindow", u"Dateimanager", None))
        self.menuAnsicht.setTitle(QCoreApplication.translate("MainWindow", u"Ansicht", None))
        self.actionSetAnzFledermause.setText(QCoreApplication.translate("MainWindow", u"Set Anz der Fledermause", None))

