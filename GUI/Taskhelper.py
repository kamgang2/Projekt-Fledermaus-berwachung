from enum import Enum
from datetime import datetime
from PySide6.QtWidgets import QSpinBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal, QObject
import time
import os
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


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
            lines.append(line.strip().split(","))

        for item in lines: 
                date = item[0].split(" ")[0]
                item[0] = date 
        
        if(sc_factor == scalefactor.Month): 
            for el in lines: 
                key = el[0].split("-")[1]

                if key not in groupedDate: 
                    groupedDate[key] = []
                groupedDate[key].append(el)

        if(sc_factor == scalefactor.Day):
            for el in lines: 
                key =  el[0].split("-")[0]+ "-" + el[0].split("-")[1]
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


def data_lesen():
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


def convert_to_datetime(value):
        try:
            # Versuchen, den Wert in ein datetime-Objekt umzuwandeln
            return datetime.strptime(value, '%d-%m-%Y %H:%M:%S')
        except ValueError:
            try:
                # Versuchen, den Wert in ein Datum ohne Uhrzeit umzuwandeln
                return datetime.strptime(value, '%d-%m-%Y').date()
            except ValueError:
                # Wenn beide Versuche fehlschlagen, den Wert als Text beibehalten
                return value



class SpinBoxDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Anzahl der Fledermauser")

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
    watch_file = os.path.join(os.path.dirname(__file__),"serial_data.txt")
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


class FileWatcher(QObject):
    file_modified = Signal()

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.observer = None
        self.thread = None

    def start(self):
        self.thread = threading.Thread(target=self.run,  daemon=True)
        self.thread.start()

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

    def stop(self):
        self.observer.stop()
                