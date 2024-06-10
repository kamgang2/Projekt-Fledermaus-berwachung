from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QLCDNumber
from PySide6.QtGui import QPixmap
from PySide6 import QtGui
from mainwindow import Ui_MainWindow
import sys 
import numpy as np 
import matplotlib.pyplot as plt 


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Verknüpfen des Plot-Buttons mit der plot_data Methode
        self.ui.plotButton.clicked.connect(self.plot_data)
       
        # Setze die Textfarbe des QLCDNumber-Widgets
        self.ui.lcdGesamtzahl.setSegmentStyle(QLCDNumber.Flat)
       
        # self.ui.lcdGesamtzahl.display(0)  # Initialisiere das Display mit 0
        # palette = self.ui.lcdGesamtzahl.palette()
        # palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor("skyblue"))  # Ändere die Textfarbe auf Rot
        # self.ui.lcdGesamtzahl.setPalette(palette)
        
        self.data = None
        self.yeinDaten = None
        self.yausDaten = None
        self.zeiten = None

    def resizeEvent(self, event):
        super(MainWindow, self).resizeEvent(event)
        # Plot neu zeichnen, wenn die Fenstergröße geändert wird
        if self.data is not None:
            self.plot_data()

    def plot_data(self):
        # Daten nur einmal einlesen
        if self.data is None:
            self.data = self.data_lesen()
            if not self.data:
                return
            self.yeinDaten, self.yausDaten, self.zeiten,self.yanzMäuser, gesamtzahl = self.process_data(self.data)

        # Größe der QGraphicsView abfragen
        view_size = self.ui.graphicsView.size()
        width, height = view_size.width(), view_size.height()

        # Plotten der Daten mit Matplotlib und dynamische Anpassung der Größe
        fig, ax = plt.subplots(figsize=(width /90 , height/ 90 ))
        ax.plot(self.zeiten, self.yeinDaten, label='Einfluege', color='green')
        ax.plot(self.zeiten, self.yausDaten, label='Ausfluege', color= 'red')
        ax.plot(self.zeiten, self.yanzMäuser, label = 'Anz Fledermausern', color = 'skyblue' )
        ax.set_xlabel('Zeit')
        ax.set_ylabel('Werte')
        ax.set_title('Ein- und Aus-Fluege über die Zeit')
        ax.legend()
        
        # Speichern des Plots in ein Bild
        plt.savefig("plot.png", bbox_inches='tight', pad_inches=0)
        plt.close(fig)
        
        # Bild in QPixmap laden
        pixmap = QPixmap("plot.png")
        
        # Erstellen einer QGraphicsScene und Hinzufügen des Bildes
        scene = QGraphicsScene()
        scene.addPixmap(pixmap)
        
        # Anzeigen der Szene in der QGraphicsView
        self.ui.graphicsView.setScene(scene)

        # Gesamtzahl 
        self.ui.lcdGesamtzahl.display(gesamtzahl)

    def data_lesen(self):
        # Öffnen der Datei im Lesemodus
        try:
            with open("serial_data.txt", "r") as myfile:
                # Initialisieren einer leeren Liste, um die Zeilen zu speichern
                lines = []
                
                # Durchlaufen jeder Zeile in der Datei
                for line in myfile:
                    # Entfernen des Zeilenumbruchs und Hinzufügen zur Liste
                    lines.append(line.strip())
                
                # Rückgabe der Liste mit den Zeilen
                return lines
        except FileNotFoundError:
            print("Datei 'serial_data.txt' nicht gefunden.")
            return []

    def process_data(self, daten):
        yeinDaten = []
        yausDaten = []
        yanzMäuser = []
        zeiten = []
        gesamtzahl = 0 

        for line in daten:
            verkehr = line.split(",")
            if len(verkehr) >= 4:
                # Extrahiert die Zeit und die Ein- und Ausgänge
                zeit = verkehr[0]
                yein = int(verkehr[1].strip().replace("->", ""))
                yaus = int(verkehr[2].strip().replace("<-", ""))
                yanz = int(verkehr[3].strip().replace("$",""))
                
                # Zeit, Ein- und Ausgänge zu den jeweiligen Listen hinzufügen
                zeiten.append(zeit)
                yeinDaten.append(yein)
                yausDaten.append(yaus)
                yanzMäuser.append(yanz)
        
        last_line = daten[-1].split(",")
        if len(last_line) >= 4: 
            gesamtzahl = int(last_line[3].strip().replace("$",""))
        # Rückgabe der Listen
        return yeinDaten, yausDaten, zeiten,yanzMäuser, gesamtzahl

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())