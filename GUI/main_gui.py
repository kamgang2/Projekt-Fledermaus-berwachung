from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene
from PySide6.QtGui import QPixmap
from ui_mainwindow import Ui_MainWindow
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
            self.yeinDaten, self.yausDaten, self.zeiten = self.process_data(self.data)

        # Größe der QGraphicsView abfragen
        view_size = self.ui.graphicsView.size()
        width, height = view_size.width(), view_size.height()

        # Plotten der Daten mit Matplotlib und dynamische Anpassung der Größe
        fig, ax = plt.subplots(figsize=(width / 100, height / 100))
        ax.plot(self.zeiten, self.yeinDaten, label='Ein Daten', color='green')
        ax.plot(self.zeiten, self.yausDaten, label='Aus Daten', color= 'red')
        ax.set_xlabel('Zeit')
        ax.set_ylabel('Werte')
        ax.set_title('Ein- und Aus-Daten über die Zeit')
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
        zeiten = []

        for line in daten:
            verkehr = line.split(",")
            if len(verkehr) >= 4:
                # Extrahiert die Zeit und die Ein- und Ausgänge
                zeit = verkehr[0]
                yein = int(verkehr[1].strip().replace("->", ""))
                yaus = int(verkehr[2].strip().replace("<-", ""))
                
                # Zeit, Ein- und Ausgänge zu den jeweiligen Listen hinzufügen
                zeiten.append(zeit)
                yeinDaten.append(yein)
                yausDaten.append(yaus)

        # Rückgabe der Listen
        return yeinDaten, yausDaten, zeiten

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())