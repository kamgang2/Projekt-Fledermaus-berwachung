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

    
"""
"""

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class OnMyWatch:
    watch_file = os.path.join(os.path.dirname(__file__), "serial_data.txt")
    file_modified = False 

    def __init__(self):
        self.observer = Observer()

    def run(self):
        print(f"Watching file: {self.watch_file}")

        if not os.path.exists(self.watch_file):
            print(f"File '{self.watch_file}' does not exist.")
            return

        event_handler = Handler()
        self.observer.schedule(event_handler, os.path.dirname(self.watch_file), recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Observer stopped")

        self.observer.join()
        return OnMyWatch.file_modified

class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return

        if event.event_type == 'modified' and event.src_path == OnMyWatch.watch_file:
            print(f"Watchdog received modified event for {event.src_path}")
            OnMyWatch.file_modified = True

        if event.event_type == 'deleted' and event.src_path == OnMyWatch.watch_file:
            print(f"Watchdog detected that {event.src_path} has been deleted.")

if __name__ == "__main__":
    watch = OnMyWatch()     

    file_modified = watch.run()
    if file_modified==True:
        print("file modified")
    else:
        print("file not modified")

    file_modified = False


"""
"""
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Erstellen des TabWidgets
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Hinzufügen der Tabs
        self.create_tabs()

    def create_tabs(self):
        # Tab 1
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        tab1_label = QLabel("Dies ist Tab 1")
        tab1_layout.addWidget(tab1_label)
        tab1.setLayout(tab1_layout)

        # Tab 2
        tab2 = QWidget()
        tab2_layout = QVBoxLayout()
        tab2_label = QLabel("Dies ist Tab 2")
        tab2_layout.addWidget(tab2_label)
        tab2.setLayout(tab2_layout)

        # Weitere Tabs können auf die gleiche Weise hinzugefügt werden

        # Hinzufügen der Tabs zum TabWidget
        self.tabs.addTab(tab1, "Tab BONO")
        self.tabs.addTab(tab2, "Tab 2")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
    """
"""
import pyqtgraph as pg
from PySide6 import QtWidgets
import numpy as np

# Erstelle eine QApplication-Instanz
app = pg.mkQApp()

# Erstelle ein Plot-Widget
win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('Mehrere Y-Achsen Beispiel')

# Erstelle zwei Plots, die dieselbe X-Achse teilen
p1 = win.addPlot()
p2 = pg.ViewBox()

# Konfiguriere die zweite Y-Achse (rechts)
p1.showAxis('right')
p1.scene().addItem(p2)
p1.getAxis('right').linkToView(p2)
p2.setXLink(p1)

# Daten generieren
x = np.linspace(0, 10, 100)
y1 = np.sin(x) * 20 + 25  # Beispiel-Daten für Temperatur (in Grad Celsius)
y2 = np.cos(x) * 50 + 50  # Beispiel-Daten für Prozentwerte

# Plotte die Daten
curve1 = p1.plot(x, y1, pen='r', name="Temperatur (°C)")
curve2 = pg.PlotDataItem(x, y2, pen='b', name="Prozent (%)")
p2.addItem(curve2)

# Synchronisiere die Ansichten
def updateViews():
    p2.setGeometry(p1.vb.sceneBoundingRect())
    p2.linkedViewChanged(p1.vb, p2.XAxis)

p1.vb.sigResized.connect(updateViews)

# Setze Achsenbezeichnungen und Bereiche
p1.setLabel('left', 'Temperatur (°C)', color='red')
p1.setLabel('bottom', 'Zeit (s)')
p1.setYRange(-10, 50, padding=0)

p1.getAxis('right').setLabel('Prozent (%)', color='blue')
p2.setYRange(0, 100, padding=0)

# Starte die Qt-Anwendung
if __name__ == '__main__':
    updateViews()
    QtWidgets.QApplication.instance().exec()
"""
"""
import serial  # install with " pip3 install pyserial"
import time
import datetime
import matplotlib.pyplot as plt
import numpy as np

# Configure the serial port and the baud rate
serial_port1 = 'COM4'  # Replace with your serial port
serial_port2 = 'COM5'
baud_rate = 9600
output_file = 'serial_data.txt'

try:
    # Open the serial port
    ser1 = serial.Serial(serial_port1, baud_rate)
    ser2 = serial.Serial(serial_port2, baud_rate)
    time.sleep(2)  # Wait for the serial connection to initialize
    print(f"Connected to {serial_port1} at {baud_rate} baud.")
    print(f"Connected to {serial_port2} at {baud_rate} baud.")
except serial.SerialException as e:
    print(f"Error opening serial port {serial_port1}: {e}")
    print(f"Error opening serial port {serial_port2}: {e}")
    exit(1)

data1 = None
data2 = None


# Open the file to write the data
with open(output_file, 'a') as file:
    try:
        while True:
            if ser1.in_waiting > 0 : 
                # Read a line from the serial port
                data1 = ser1.readline().decode('utf-8').strip() 
                print(f"Received from {serial_port1}: {data1}")
                ##timestamp = datetime.datetime.now()
                # Print the line to the console
                #myDataLine =timestamp.strftime("%d-%m-%Y %H:%M:%S")+","+ line1 
            
                # Write the line to the file
                # file.write(myDataLine + '\n')

            if ser2.in_waiting > 0:
                data2 = ser2.readline().decode('utf-8').strip()
                print(f"received from{serial_port2}: {data2}")

            if data1 is not None and data2 is not None:
                timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                myDataLine = f"{timestamp},{data1},{data2}"
                print(f"Writing to file: {myDataLine}")
                file.write(myDataLine + '\n')
                file.flush()  # Ensure the data is written to the file immediately
                # Reset the data after writing
                data1 = None
                data2 = None
                time.sleep(1)  # Add a small delay to prevent high CPU usage

            else:
                print("No data waiting in the serial buffer.")
            time.sleep(1)  # Add a small delay to prevent high CPU usage
    except KeyboardInterrupt:
        print("Program interrupted. Closing...")
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
    finally:
        ser1.close()
        ser2.close()
        print(f"Disconnected from {serial_port1} and {serial_port2}.")   

"""
"""
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QMainWindow
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtGui import QPixmap, QPalette, QColor
from PySide6.QtCore import QUrl, Slot
import sys


class VideoSplashScreen(QDialog):
    def __init__(self, video_file, image_file, parent=None):
        super(VideoSplashScreen, self).__init__(parent)
        self.setWindowTitle("Splash Screen")

        # Create a layout
        self.layout = QVBoxLayout(self)

        # Create a video widget
        self.video_widget = QVideoWidget(self)
        self.layout.addWidget(self.video_widget)

        # Create a media player
        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setAudioOutput(self.audio_output)

        # Load the video file
        self.media_player.setSource(QUrl.fromLocalFile(video_file))

        # Connect signals
        self.media_player.mediaStatusChanged.connect(self.media_status_changed)
        self.media_player.errorOccurred.connect(self.handle_error)

        # Play the video
        self.media_player.play()

        # Initialize the image and start button for later use
        self.image_file = image_file
        self.image_label = None
        self.start_button = None

    @Slot(QMediaPlayer.MediaStatus)
    def media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            # Hide the video widget
            self.video_widget.hide()

            # Set background image
            self.set_background_image(self.image_file)

            # Show the start button
            self.show_start_button()

    @Slot()
    def handle_error(self):
        print("Error occurred:", self.media_player.errorString())

    def set_background_image(self, image_file):
        # Create a label to hold the image
        self.image_label = QLabel(self)
        pixmap = QPixmap(image_file)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.layout.addWidget(self.image_label)
        self.image_label.show()

    def show_start_button(self):
        # Add a start button
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.accept)  # Close dialog on button click
        self.layout.addWidget(self.start_button)
        self.start_button.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Main Application")
        self.setGeometry(100, 100, 800, 600)
        # Add more UI setup here if needed


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and show the combined splash screen
    splash = VideoSplashScreen("0728.mp4", "icons/gui_icon.png")
    if splash.exec() == QDialog.Accepted:
        # Show the main window after the splash screen
        main_window = MainWindow()
        main_window.show()

    sys.exit(app.exec())

"""

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLCDNumber
from PySide6.QtCore import QPropertyAnimation, QRect, Qt
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Hauptfenster-Einstellungen
        self.setWindowTitle("Seitenbereich von rechts nach links")
        self.setGeometry(100, 100, 800, 600)

        # Hauptwidget und Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Button zum Öffnen/Schließen des Seitenbereichs
        self.toggle_button = QPushButton("Toggle Sidebar")
        layout.addWidget(self.toggle_button)
        self.toggle_button.clicked.connect(self.toggle_sidebar)

        # Seitenbereich
        self.sidebar = QWidget(self)
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("background-color: lightgray;")
        self.sidebar.move(800, 0)

        # Seitenbereichs-Layout
        sidebar_layout = QVBoxLayout(self.sidebar)

        # LCD-Anzeige
        self.lcd_display = QLCDNumber()
        self.lcd_display1 = QLCDNumber()
        sidebar_layout.addWidget(self.lcd_display)
        sidebar_layout.addWidget(self.lcd_display1)

        # Animation
        self.animation = QPropertyAnimation(self.sidebar, b"geometry")
        self.animation.setDuration(500)

        # Initialer Zustand der Seitenleiste
        self.sidebar_open = False

    def toggle_sidebar(self):
        if self.sidebar_open:
            # Seitenbereich schließen
            self.animation.setStartValue(QRect(600, 0, 200, 600))
            self.animation.setEndValue(QRect(800, 0, 200, 600))
            self.sidebar_open = False
        else:
            # Seitenbereich öffnen
            self.animation.setStartValue(QRect(800, 0, 200, 600))
            self.animation.setEndValue(QRect(600, 0, 200, 600))
            self.sidebar_open = True

        self.animation.start()

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()



"""
def data_lesen(lese_datei):
    try:
        with open(lese_datei, "r") as myfile:
            # Initialize an empty list to store lines
            lines = []
            
            # Iterate over each line in the file
            for line in myfile:
                # Strip whitespace and check if line ends with a semicolon
                line = line.strip()
                if line.endswith(";"):
                    # Add the line to the list if it ends with a semicolon
                    lines.append(line)
            
            # Return the list of lines
            return lines
    except FileNotFoundError:
        print(f"Datei {lese_datei} nicht gefunden.")
        return []
"""