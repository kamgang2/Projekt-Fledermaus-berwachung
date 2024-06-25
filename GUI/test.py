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

            # for key, group in groupedDate.items(): 
            #         print(f"Group {key}:")
            #         for item in group:
            #             print (item)
            return groupedDate

    except FileNotFoundError:
        print("File not found: 'serial_data.txt'")

# Call the function to execute it

# data = timescaling("day")
# for key, group in data.items():
#     print(f"Group {key}:")
#     for item in group:          
#         print (item)
  

def getAverage(data, whichValue):
    averages = {}
    
    for key, group in data.items():
        total_value = 0
        count = 0
        
        for item in group:
            if whichValue == "ein":
                value = int(item[1].replace("->", "").strip())
                total_value += value
                count += 1

            if whichValue == "aus":
                value = int(item[2].replace("<-","").strip())
                total_value += value
                count += 1

            if whichValue == "sum":
                value = int(item[3].replace("$","").strip())
                total_value += value
                count += 1
            
            if whichValue == "hydr":
                value = int(item[4].replace("%","").strip())
                total_value += value
                count += 1

            if whichValue == "temp":
                value = int(item[5].replace("C","").strip())
                total_value += value
                count += 1

        if count > 0:
            average_value = total_value / count
            averages[key] = average_value
        else:
            averages[key] = 0

    return averages


data = timescaling("day")
averages = getAverage(data, "ein")
for key, average in averages.items():
    print(f"Gruppe: {key}, Durchschnittswert: {average}")

    """
"""
import pyqtgraph.examples
pyqtgraph.examples.run()
"""
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSpinBox, QLabel
import sys

class SpinBoxApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('SpinBox Example')
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()

        self.button = QPushButton('Show SpinBox')
        self.button.clicked.connect(self.show_spinbox)

        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(0)
        self.spinbox.setMaximum(100)
        self.spinbox.setVisible(False)

        self.get_value_button = QPushButton('Get SpinBox Value')
        self.get_value_button.clicked.connect(self.get_spinbox_value)
        self.get_value_button.setVisible(False)

        self.value_label = QLabel('')

        self.layout.addWidget(self.button)
        self.layout.addWidget(self.spinbox)
        self.layout.addWidget(self.get_value_button)
        self.layout.addWidget(self.value_label)

        self.setLayout(self.layout)

    def show_spinbox(self):
        self.spinbox.setVisible(True)
        self.get_value_button.setVisible(True)

    def get_spinbox_value(self):
        value = self.spinbox.value()
        self.value_label.setText(f'SpinBox Value: {value}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SpinBoxApp()
    window.show()
    sys.exit(app.exec())
