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
"""   

# grouped_xmos = {}

# for file in filtered_files:
#     xmos_names = file['filename']
#     xmos_name = xmos_names[3]
#     key = f"{xmos_name}"
    
#     if key not in grouped_xmos:
#         grouped_xmos[key] = []
    
#     grouped_xmos[key].append(file)



"""
def timescaling(scalefactor): 
    try:
        with open("serial_data.txt", "r") as myfile: 
            lines = []
            groupedDate = {}

            for line in myfile:     
                lines.append(line.strip().split(","))

            for item in lines: 
                    date = item[0].split(" ")[0]
                    item[0] = date
            
            if(scalefactor== "month"): 
                for el in lines: 
                    key = el[0].split("-")[1]

                    if key not in groupedDate: 
                        groupedDate[key] = []
                    groupedDate[key].append(el)

            if(scalefactor == "day"):
                for el in lines: 
                    key =  el[0].split("-")[0]+ "-" + el[0].split("-")[1]
                    if key not in groupedDate: 
                        groupedDate[key]=[]
                    groupedDate[key].append(el)

            for key, group in groupedDate.items(): 
                    print(f"Group {key}:")
                    for item in group:
                        print(item)

    except FileNotFoundError:
        print("File not found: 'serial_data.txt'")

# Call the function to execute it
timescaling("day")


"""  

import sys
import time
import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QLCDNumber
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer, Slot
from PySide6 import QtGui
import numpy as np
import matplotlib.pyplot as plt
from GuiAnwendung.gui.mainwindow import Ui_MainWindow
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, callback):
        super(FileChangeHandler, self).__init__()
        self.callback = callback

    def on_modified(self, event):
        if event.src_path.endswith("serial_data.txt"):
            self.callback()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Verknüpfen des Plot-Buttons mit der plot_data Methode
        self.ui.plotButton.clicked.connect(self.plot_data)
       
        # Setze die Textfarbe des QLCDNumber-Widgets
        self.ui.lcdGesamtzahl.setSegmentStyle(QLCDNumber.Flat)
       
        self.data = None
        self.yeinDaten = None
        self.yausDaten = None
        self.zeiten = None

        # Set up file system observer
        self.event_handler = FileChangeHandler(self.update_data)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path='.', recursive=False)
        self.observer.start()

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
            self.yeinDaten, self.yausDaten, self.zeiten, self.yanzMäuser, gesamtzahl, LuftFeuchtigkeit, Temp = self.process_data(self.data)

        # Größe der QGraphicsView abfragen
        view_size = self.ui.graphicsView.size()
        width, height = view_size.width(), view_size.height()

        # Plotten der Daten mit Matplotlib und dynamische Anpassung der Größe
        fig, ax = plt.subplots(figsize=(width / 90, height / 90))
        ax.plot(self.zeiten, self.yeinDaten, label='Einfluege', color='green')
        ax.plot(self.zeiten, self.yausDaten, label='Ausfluege', color='red')
        ax.plot(self.zeiten, self.yanzMäuser, label='Anz Fledermausern', color='skyblue')
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
        Temp = 0 
        LuftFeuchtigkeit = 0 

        for line in daten:
            verkehr = line.split(",")
            if len(verkehr) >= 6:
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
        if len(last_line) >= 6: 
            gesamtzahl = int(last_line[3].strip().replace("$",""))
            LuftFeuchtigkeit = float(last_line[4].strip().replace("%",""))
            Temp = float(last_line[5].strip().replace("°C",""))

        # Rückgabe der Listen
        return yeinDaten, yausDaten, zeiten, yanzMäuser, gesamtzahl, LuftFeuchtigkeit, Temp

    @Slot()
    def update_data(self):
        # Read the latest data and update the plot and LCD displays
        self.data = self.data_lesen()
        if not self.data:
            return
        self.yeinDaten, self.yausDaten, self.zeiten, self.yanzMäuser, gesamtzahl, LuftFeuchtigkeit, Temp = self.process_data(self.data)

        self.plot_data()
        self.ui.lcdGesamtzahl.display(gesamtzahl)
        self.ui.lcdTemp.display(Temp)
        self.ui.lcdLuft.display(LuftFeuchtigkeit)

    def closeEvent(self, event):
        self.observer.stop()
        self.observer.join()
        super(MainWindow, self).closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
