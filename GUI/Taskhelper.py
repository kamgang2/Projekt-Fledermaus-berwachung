from enum import Enum
from datetime import datetime
from PySide6.QtWidgets import QSpinBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QLCDNumber
from PySide6.QtCore import Signal, QObject, QThread, QPropertyAnimation, QRect
import time
import os
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys


# resource_path Funktion, um den Pfad zu eingebetteten Dateien zu finden
def resource_path(relative_path):
    """Ermittelt den Pfad zur eingebetteten Datei in einer .exe-Datei."""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller speichert Ressourcen im temporären Verzeichnis _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class scalefactor(Enum): 
    Normal =1 
    Day = 2
    Month = 3

class Eigenschaften(Enum):
    Eingaenge = 1
    Ausgaenge = 2
    Summe = 3 
    Luftfeuchtigkeit = 4
    Temperatur = 5
    

def timescaling(myfile,  sc_factor: scalefactor): 
    try:
        
        lines = []
        groupedDate = {}

        for line in myfile: 
            line_splited = line.strip().split(",")  
            lines.append(line_splited)

        for item in lines: 
                date = item[0].split(" ")[0]
                item[0] = date 
        
        if(sc_factor == scalefactor.Month): 
            for el in lines: 
                key = el[0].split(".")[1]+ "."+ el[0].split(".")[2]

                if key not in groupedDate: 
                    groupedDate[key] = []
                groupedDate[key].append(el)

        if(sc_factor == scalefactor.Day):
            for el in lines: 
                key =  el[0].split(".")[0]+ "."+ el[0].split(".")[1] + "." + el[0].split(".")[2]
                if key not in groupedDate: 
                    groupedDate[key]=[]
                groupedDate[key].append(el)

        if(sc_factor == scalefactor.Normal): 
            groupedDate = myfile

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
  

def getAverage(data, whichValue : Eigenschaften):
    averages = {}
    
    for key, group in data.items():
        total_value = 0
        count = 0
        
        for item in group:
            if len(item) >= 6:
                if whichValue == Eigenschaften.Eingaenge:
                    value = int(item[1].replace("->", "").strip())
                    total_value += value
                    count += 1

                if whichValue == Eigenschaften.Ausgaenge:
                    value = int(item[2].replace("<-","").strip())
                    total_value += value
                    count += 1

                if whichValue == Eigenschaften.Summe:
                    value = int(item[3].replace("$","").strip())
                    total_value += value
                    count += 1
                
                if whichValue == Eigenschaften.Luftfeuchtigkeit:
                    value = float(item[4].replace("%","").strip())
                    total_value += value
                    count += 1

                if whichValue == Eigenschaften.Temperatur:
                    value = float(item[5].replace("C","").strip())
                    total_value += value
                    count += 1

        if count > 0:
            average_value = total_value / count
            averages[key] = average_value
        else:
            averages[key] = 0

    return averages


# data = timescaling("day")
# averages = getAverage(data, "ein")
# for key, average in averages.items():
#     print(f"Gruppe: {key}, Durchschnittswert: {average}")



def process_average_data(daten):
    zeiten, yeinDaten, yausDaten, yanzMäuser, yTemp, yLuft = [], [], [], [], [], []
    averagesEin = getAverage(daten, Eigenschaften.Eingaenge)
    averagesAus = getAverage(daten, Eigenschaften.Ausgaenge)
    averageSum = getAverage(daten, Eigenschaften.Summe)
    averageTemp = getAverage(daten, Eigenschaften.Temperatur)
    averageLuft_F = getAverage(daten, Eigenschaften.Luftfeuchtigkeit)

    for key in daten.keys():
        zeiten.append(key)
        yeinDaten.append(averagesEin.get(key, 0))
        yausDaten.append(averagesAus.get(key, 0))
        yanzMäuser.append(averageSum.get(key, 0))
        yTemp.append(averageTemp.get(key,0))
        yLuft.append(averageLuft_F.get(key, 0))
    
    return zeiten, yeinDaten, yausDaten, yanzMäuser, yTemp, yLuft

def read_single_Tempvalue(daten): 
    the_last_line = daten[-1]
    the_last_line_splited = the_last_line.split(",")
    Temp1= the_last_line_splited[6].strip().replace("T1", "")
    Temp2= the_last_line_splited[7].strip().replace("T2", "")
    Temp3= the_last_line_splited[8].strip().replace("T3", "")
    Hum1= the_last_line_splited[9].strip().replace("H1", "")
    Hum2= the_last_line_splited[10].strip().replace("H2", "")
    Hum3= the_last_line_splited[11].strip().replace("H3", "")
     
    return Temp1, Temp2, Temp3, Hum1, Hum2, Hum3

def convert_to_datetime(value):
        try:
            # Versuchen, den Wert in ein datetime-Objekt umzuwandeln
            return datetime.strptime(value, '%d.%m.%Y %H:%M:%S')
        except ValueError:
            try:
                # Versuchen, den Wert in ein Datum ohne Uhrzeit umzuwandeln
                return datetime.strptime(value, '%d.%m.%Y').date()
            except ValueError:
                # Wenn beide Versuche fehlschlagen, den Wert als Text beibehalten
                return value



class SpinBoxDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Anzahl der Fledermauser")
        # Load and apply the stylesheet
        with open(resource_path('style.qss'), 'r') as file:

            self.setStyleSheet(file.read())

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Geben die Anzahl der Fledermausern ein:")
        self.layout.addWidget(self.label)

        self.spinbox = QSpinBox(self)
        self.spinbox.setRange(0, 1000)
        self.layout.addWidget(self.spinbox)

        self.button_layout = QHBoxLayout()

        self.button_ok = QPushButton("OK")
        self.button_ok.clicked.connect(self.accept)
        self.button_layout.addWidget(self.button_ok)

        self.button_cancel = QPushButton("Abbrechen")
        self.button_cancel.clicked.connect(self.reject)
        self.button_layout.addWidget(self.button_cancel)
        
        self.layout.addLayout(self.button_layout)

    def get_value(self):
        return self.spinbox.value()
    
# Funktion zur Uberwachung des "serial_data.txt"

class OnMyWatch: 
    watch_file = os.path.join(os.path.dirname(__file__),resource_path("serial_data.txt"))
    file_modified = False

    def __init__(self):
        self.observer = Observer()

    def run(self):
        print(f"Watching file: {self.watch_file}")

        if not os.path.exists(self.watch_file):
            print(f"File '{self.watch_file}' does not exist.")
            return
        
        event_handler = Handler()
        self.observer.schedule(event_handler,  os.path.dirname(self.watch_file), recursive=False)
        self.observer.start()
        try: 
            time.sleep(5)
        except KeyboardInterrupt: 
            self.observer.stop()
            print("file`s observer stopped")

        self.observer.join()
        return OnMyWatch.file_modified
    

class Handler(FileSystemEventHandler): 
    def __init__(self, file_modified_signal):
        super().__init__()
        self.file_modified_signal = file_modified_signal

    def on_any_event(self, event):
        if event.is_directory:
            return

        if event.event_type == 'modified' and event.src_path == OnMyWatch.watch_file:
            print(f"Watchdog received modified event for {event.src_path}")
            self.file_modified_signal.emit()

        if event.event_type == 'deleted' and event.src_path == OnMyWatch.watch_file:
            print(f"Watchdog detected that {event.src_path} has been deleted.")


class FileWatcher(QThread):
    file_modified = Signal()

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.observer = None
        self.thread = None

    def start(self):
        self.thread = threading.Thread(target=self.run,  daemon=True)
        self.thread.start()
        print("file watcher Thread gestartet")

    def run(self):
        event_handler = Handler(self.file_modified)
        self.observer = Observer()
        self.observer.schedule(event_handler, os.path.dirname(self.file_path), recursive=False)
        self.observer.start()
        print(f"Watching file: {self.file_path}")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()

        self.observer.join()
        print("File watcher thread stopped.")

    def stop(self):
        if self.observer:
            self.observer.stop()

                

class SerialMonitorThread(QThread):
    warning_signal = Signal(str, str)
    
    def __init__(self, serial_port1, serial_port2, ser1, ser2):
        super().__init__()
        self.serial_port1 = serial_port1
        self.serial_port2 = serial_port2
        self.ser1 = ser1
        self.ser2 = ser2

    def run(self):
            if not self.ser1 :
                self.warning_signal.emit("Serial Port Error", f"Serial port {self.serial_port1} is not available.")
                self.ser1 = None
            if not self.ser2:
                self.warning_signal.emit("Serial Port Error", f"Serial port {self.serial_port2} is not available.")
                self.ser2 = None

