"""
import numpy as np
import matplotlib.pyplot as plt
import os

 
def plot_data(daten):
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

    # Umwandeln der Listen in numpy-Arrays
    zeiten = np.array(zeiten)
    yeinDaten = np.array(yeinDaten)
    yausDaten = np.array(yausDaten)
    
    # Plotten der Daten
    plt.figure(figsize=(10, 5))
    plt.plot(zeiten, yeinDaten, label='Ein Daten')
    plt.plot(zeiten, yausDaten, label='Aus Daten')
    plt.xlabel('Zeit')
    plt.ylabel('Werte')
    plt.title('Ein- und Aus-Daten über die Zeit')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



def data_lesen():

    print("Aktuelles Arbeitsverzeichnis:", os.getcwd())
    
    # Absoluter Pfad zur Datei
    file_path = os.path.join(os.getcwd(), "serial_data.txt")
    
    # Überprüfen, ob die Datei existiert
    if not os.path.isfile(file_path):
        print(f"Datei {file_path} existiert nicht.")
        return []
    # Öffnen der Datei im Lesemodus
    with open("serial_data.txt", "r") as myfile:
        # Initialisieren einer leeren Liste, um die Zeilen zu speichern
        lines = []
        
        # Durchlaufen jeder Zeile in der Datei
        for line in myfile:
            # Entfernen des Zeilenumbruchs und Hinzufügen zur Liste
            lines.append(line.strip())
    
    # Rückgabe der Liste mit den Zeilen
    return lines


# Beispielaufruf der Funktion mit Daten aus der Datei
data = data_lesen()
plot_data(data)
"""

from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, QRect, QTimer
import sys

class CircularProgress(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = 0
        self.setMinimumSize(200, 200)

    def setValue(self, value):
        self.value = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = QRect(10, 10, self.width() - 20, self.height() - 20)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Hintergrundkreis
        pen = QPen(Qt.gray, 10)
        painter.setPen(pen)
        painter.drawEllipse(rect)

        # Fortschrittskreis
        pen.setColor(Qt.blue)
        painter.setPen(pen)
        painter.drawArc(rect, 90 * 16, -self.value * 16 * 3.6)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.progress = CircularProgress()
        
        layout = QVBoxLayout()
        layout.addWidget(self.progress)
        self.setLayout(layout)

        # Timer für die Aktualisierung des Fortschritts
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)

        self.progress_value = 0

    def update_progress(self):
        self.progress_value += 1
        if self.progress_value > 100:
            self.progress_value = 0
        self.progress.setValue(self.progress_value)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
