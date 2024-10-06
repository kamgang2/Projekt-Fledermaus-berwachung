from PySide6.QtWidgets import QApplication, QMainWindow, QLCDNumber, QSpinBox, QDialog, QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QDateEdit, QMessageBox, QPushButton, QFrame, QGridLayout
from PySide6.QtGui import QPixmap, QActionGroup, QColor, QFontDatabase, QFont, QIcon
from mainwindow import Ui_MainWindow  
from Taskhelper import timescaling, scalefactor, process_average_data, convert_to_datetime,read_single_Tempvalue, SpinBoxDialog,FileWatcher, SerialMonitorThread
from file_handler import file_writter, data_lesen, data_lesen_zeitraum, FileWriterWorker
from splashscreen import VideoSplashScreen
import sys
import pyqtgraph as pg
from PySide6.QtCore import Qt, Slot, QRect, QPropertyAnimation, QThread
from PySide6 import QtConcurrent
import serial
import os
import time
import threading
import serial


class CustomAxisItem(pg.AxisItem):
    def __init__(self, labels=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.labels = labels if labels is not None else {}

    def tickStrings(self, values, scale, spacing):
        strings = []
        for v in values:
            v_str = self.labels.get(v, "")
            strings.append(v_str)
        return strings



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.lock = threading.Lock() 
        self.setWindowTitle("FLEDERMAUSTRACKER")

        self.setWindowIcon(QIcon("icons/gui_icon.png"))


       # Configure the serial port and the baud rate
        self.serial_port1 = 'COM4'  # Replace with your serial port
        self.serial_port2 = 'COM9'
        self.baud_rate = 9600
        self.output_file = 'serial_data.txt'
        
        try:
            # Open the serial port
            self.ser1 = serial.Serial(self.serial_port1, self.baud_rate)
            self.ser2 = serial.Serial(self.serial_port2, self.baud_rate)
            time.sleep(2)  # Wait for the serial connection to initialize
            print(f"Connected to {self.serial_port1} at {self.baud_rate} baud.")
            print(f"Connected to {self.serial_port2} at {self.baud_rate} baud.")
        except serial.SerialException as e:
            print(f"Error opening serial port {self.serial_port1}: {e}")
            print(f"Error opening serial port {self.serial_port2}: {e}")
            self.show_message()
            self.ser1 = None
            self.ser2 = None
            

        self.ui.setupUi(self)

        # # Hintergrundfarbe als hexadezimale Zeichenkette
        # hex_color = "#E9F1FA"

        # # # Konvertieren Sie die hexadezimale Zeichenkette in ein QColor-Objekt
        # color = QColor(hex_color)
        self.ui.plotWidget1.setBackground('w')
        self.ui.plotWidget2.setBackground('w')

        self.ui.tabWidget.currentChanged.connect(self.onTabChanged)

        # Set segment style of QLCDNumber widget
        self.ui.lcdGesamtzahl.setSegmentStyle(QLCDNumber.Flat)

        self.data = None
        self.yeinDaten = None
        self.yausDaten = None
        self.zeiten = None
        self.yTemp = None 
        self.yLuft = None
        self.gesamtzahl = 0
        self.LuftFeuchtigkeit = 0
        self.Temp = 0
        self.Temp1 = 0
        self.Temp2 = 0
        self.Temp3 = 0
        self.Hum1 = 0 
        self.Hum2 = 0
        self.Hum3 = 0

        self.spinbox = QSpinBox()
        self.spinbox.setVisible(False)

        # Create QActionGroup for mutually exclusive actions
        self.scaleActionGroup = QActionGroup(self)
        self.scaleActionGroup.setExclusive(True)

        # Make actions checkable
        self.ui.actionNormal.setCheckable(True)
        self.ui.actionTag.setCheckable(True)
        self.ui.actionMonat.setCheckable(True)

        self.ui.actionNormal.triggered.connect(self.plot_data)
        self.ui.actionTag.triggered.connect(self.plot_data)
        self.ui.actionMonat.triggered.connect(self.plot_data)
        

        # Add actions to the group
        self.scaleActionGroup.addAction(self.ui.actionNormal)
        self.scaleActionGroup.addAction(self.ui.actionTag)
        self.scaleActionGroup.addAction(self.ui.actionMonat)

        # Set the default checked action
        self.ui.actionNormal.setChecked(True)

        # Spinbox Dialog
        self.spinbox_dialog = SpinBoxDialog(self)

        # Set value of the Bats
        self.ui.actionSetAnzFledermause.triggered.connect(self.show_spinbox_dialog)

        # Save the Data in Excel file 
        self.ui.actionExportExcel.triggered.connect(self.data_in_excel_speichern)

        # Backup Datei löschen
        self.ui.actionDateiLoeschen.triggered.connect( self.clear_text_file)
        
        #open the sidebar
          # Seitenbereich
        self.sidebar = QFrame(self)
        self.sidebar.setStyleSheet("background-color: #E9F1FA;")
        self.sidebar.setFixedWidth(400)
        self.sidebar.move(800, 0)

        # Seitenbereichs-Layout
        sidebar_layout = QGridLayout(self.sidebar)

        # Erste LCD-Anzeige
        self.lcd_first_temp = QLCDNumber()
        self.lcd_first_temp.setStyleSheet("color: black; border-radius: 16px; background: #00ABE4;")
        self.lcd_first_temp_label = QLabel("Temp1")
        self.lcd_first_temp_label.setStyleSheet("font-family: 'Arial';font-size: 16px;")
        sidebar_layout.addWidget(self.lcd_first_temp,0,0, 1, 3)
        sidebar_layout.addWidget(self.lcd_first_temp_label, 1, 0, 1,1 )

        # Zweite LCD-Anzeige
        self.lcd_sec_temp = QLCDNumber()
        self.lcd_sec_temp.setStyleSheet("color: black; border-radius: 16px; background: #00ABE4;")
        self.lcd_sec_temp_label = QLabel("Temp2")
        self.lcd_sec_temp_label.setStyleSheet("font-family: 'Arial';font-size: 16px;")
        sidebar_layout.addWidget(self.lcd_sec_temp, 2, 0, 1, 3)
        sidebar_layout.addWidget(self.lcd_sec_temp_label, 3,0,1,1)

        # Dritte LCD-Anzeige
        self.lcd_third_temp = QLCDNumber()
        self.lcd_third_temp.setStyleSheet("color: black; border-radius: 16px; background: #00ABE4;")
        self.lcd_third_temp_label = QLabel("Temp2")
        self.lcd_third_temp_label.setStyleSheet("font-family: 'Arial';font-size: 16px;")
        sidebar_layout.addWidget(self.lcd_third_temp, 4, 0, 1, 3)
        sidebar_layout.addWidget(self.lcd_third_temp_label, 5,0,1,1)

        # 2 Column Erste LCD
        self.lcd_first_hum = QLCDNumber()
        self.lcd_first_hum.setStyleSheet("color: black; border-radius: 16px; background: #00ABE4;")
        self.lcd_first_hum_label = QLabel("HUM 1")
        self.lcd_first_hum_label.setStyleSheet("font-family: 'Arial';font-size: 16px;")
        sidebar_layout.addWidget(self.lcd_first_hum,0,3, 1, 3)
        sidebar_layout.addWidget(self.lcd_first_hum_label, 1, 3, 1,1 )

        # 2 Column Zweite LCD-Anzeige
        self.lcd_sec_hum = QLCDNumber()
        self.lcd_sec_hum.setStyleSheet("color: black; border-radius: 16px; background: #00ABE4;")
        self.lcd_sec_hum_label = QLabel("HUM 2")
        self.lcd_sec_hum_label.setStyleSheet("font-family: 'Arial';font-size: 16px;")
        sidebar_layout.addWidget(self.lcd_sec_hum, 2, 3, 1, 3)
        sidebar_layout.addWidget(self.lcd_sec_hum_label, 3,3,1,1)

        # 2 Column Dritte LCD-Anzeige
        self.lcd_third_hum = QLCDNumber()
        self.lcd_third_hum.setStyleSheet("color: black; border-radius: 16px; background: #00ABE4;")
        self.lcd_third_hum_label = QLabel("HUM 3")
        self.lcd_third_hum_label.setStyleSheet("font-family: 'Arial';font-size: 16px;")
        sidebar_layout.addWidget(self.lcd_third_hum, 4, 3, 1, 3)
        sidebar_layout.addWidget(self.lcd_third_hum_label, 5,3,1,1)

        # Schließen-Button erstellen
        close_button = QPushButton("Schließen")
        close_button.setStyleSheet("background-color: red; color: white;")
        close_button.clicked.connect(self.toggle_sidebar)

        # Button zum Layout hinzufügen
        sidebar_layout.addWidget(close_button, 6,3, 1, 1)



        # Animation
        self.animation = QPropertyAnimation(self.sidebar, b"geometry")
        self.animation.setDuration(500)

        # Initialer Zustand der Seitenleiste
        self.sidebar_open = False
        self.ui.toggle_sidebar_action.triggered.connect(self.toggle_sidebar)

        self.ui.plotWidget1.scene().sigMouseMoved.connect(self.onMouseMoved)
        self.ui.plotWidget2.scene().sigMouseMoved.connect(self.onMouseMoved)

        # Connect plot button with plot_data method
        self.plot_data()
        self.ui.plotButton.clicked.connect(self.plot_data)
        
         
        #self.start_file_writer()
        
        self.file_watcher = FileWatcher(os.path.join(os.path.dirname(__file__),  self.output_file))
        self.file_watcher.start()
        self.file_watcher.file_modified.connect(self.on_file_modified)
       

        # self.serial_monitor_thread = threading.Thread(target=self.monitor_serial_ports, daemon=True)
        # self.serial_monitor_thread.start()


    def show_spinbox_dialog(self):
        if self.spinbox_dialog.exec() == QDialog.Accepted:
            value = self.spinbox_dialog.get_value()
            self.set_anz_fledermause(value)
            self.repaint()
    
    def set_anz_fledermause(self, value):
        try: 
            zuSendendeDaten = "PY: "+str(value)
            self.ser1.write(zuSendendeDaten.encode())
            self.ser1.write("\n".encode())
            print(f"startwert_fleder: {value}")
            print(zuSendendeDaten)
        except :
            print("Error with com port")

    def get_action_checked(self):
        if self.ui.actionNormal.isChecked():
            return scalefactor.Normal
        if self.ui.actionTag.isChecked():
            return scalefactor.Day
        if self.ui.actionMonat.isChecked():
            return scalefactor.Month

    def resizeEvent(self, event):
        super(MainWindow, self).resizeEvent(event)
        # Redraw plot when window size changes
        if self.data is not None:
            self.plot_data()

    @Slot()
    def on_file_modified(self):
        print("File modification detected. Updating plot.")
        self.plot_data()

    def plot_data(self):
        self.ui.plotWidget1.clear()
        self.ui.plotWidget2.clear()
        self.ui.viewBox.clear()

        # Plotwidget2 
        p1 = self.ui.plotWidget2
        p2 =  self.ui.viewBox 

        self.data = data_lesen(self.output_file)
        if not self.data:
            return
        self.zeiten, self.yeinDaten, self.yausDaten, self.yanzMäuser,self.yTemp, self.yLuft, gesamtzahl, LuftFeuchtigkeit, Temp = self.process_data(self.data, self.get_action_checked())
        
        self.Temp1, self.Temp2, self.Temp3, self.Hum1, self.Hum2, self.Hum3 = read_single_Tempvalue(self.data)
        self.lcd_first_temp.display(self.Temp1)
        self.lcd_sec_temp.display(self.Temp2)
        self.lcd_third_temp.display(self.Temp3)
        self.lcd_first_hum.display(self.Hum1)
        self.lcd_sec_hum.display(self.Hum2)
        self.lcd_third_hum.display(self.Hum3)

        # Convert times to datetime
        self.zeiten = [convert_to_datetime(x) for x in self.zeiten]

        # Create a mapping from time to index for custom axis labels
        time_to_index = {t: i for i, t in enumerate(self.zeiten)}
        indices = [time_to_index[t] for t in self.zeiten]

        # Clear existing plots and add legends
        self.ui.plotWidget1.clear()
        self.ui.plotWidget2.clear()
        self.ui.plotWidget1.addLegend()
        self.ui.plotWidget2.addLegend()

        # Define pens with different thickness
        pen_ein = {'color': 'g', 'width': 3}  # Thickness for 'Einfluege'
        pen_aus = {'color': 'r', 'width': 3}  # Thickness for 'Ausfluege'
        pen_anz = {'color': 'b', 'width': 3}  # Thickness for 'Anz Fledermaeuser'
        pen_temp = pg.mkPen(color = 'r', width = 3)
        pen_luft = pg.mkPen(color = 'b', width = 3)

        self.ui.plotWidget1.plot(indices, self.yeinDaten, pen=pen_ein, name='Einfluege')
        self.ui.plotWidget1.plot(indices, self.yausDaten, pen=pen_aus, name='Ausfluege')
        self.ui.plotWidget1.plot(indices, self.yanzMäuser, pen=pen_anz, name='Anz Fledermaeuser')

        # Use CustomAxisItem to correctly display custom labels on the x-axis
        date_labels = {i: str(t) for i, t in enumerate(self.zeiten)}
        custom_axis = CustomAxisItem(labels=date_labels, orientation='bottom')
        self.ui.plotWidget1.setAxisItems({'bottom': custom_axis})
    
        p1.showAxis('right')
        #p1.scene().addItem(p2)
        p1.getAxis('right').linkToView(p2)
        p2.setXLink(p1)

        p1.plot(indices, self.yTemp, pen=pen_temp, name='Temperature (°C)')
        # Plot data on the secondary view (p2) and add to the legend of plotWidget2
        temp_curve = pg.PlotDataItem(indices, self.yLuft, pen=pen_luft, name="Luftfeuchtigkeit (%)")
        p2.addItem(temp_curve)
       # self.ui.plotWidget2.addItem(temp_curve)

        def updateViews():
            p2.setGeometry(p1.getViewBox().sceneBoundingRect())
            p2.linkedViewChanged(p1.getViewBox(), p2.XAxis)

        p1.getViewBox().sigResized.connect(updateViews)
        #p1.setLabel('bottom', 'Zeit')
        #p1.setLabel('left', 'Temperatur (°C)')
        p1.setTitle('Temperature und Luftfeuchtigkeit über die Zeit')
        p1.setYRange(-10, 50, padding=0)
        #p1.getAxis('right').setLabel('Luftfeuchtigkeit (%)', color='blue')
        p2.setYRange(0, 100, padding=0)
        
        # Use CustomAxisItem to correctly display custom labels on the x-axis for plotWidget2
        date_labels_plotWidget2 = {i: str(t) for i, t in enumerate(self.zeiten)}
        custom_axis_plotWidget2 = CustomAxisItem(labels=date_labels_plotWidget2, orientation='bottom')
        p1.setAxisItems({'bottom': custom_axis_plotWidget2})


        # Display total count
        self.ui.lcdGesamtzahl.display(gesamtzahl)

        # Display temperature
        self.ui.lcdTemp.display(Temp)

        # Display humidity
        self.ui.lcdLuft.display(LuftFeuchtigkeit)
        self.ui.LuftProgessBar.setValue(LuftFeuchtigkeit)
        self.ui.LuftProgessBar.setStyleSheet("QProgressBar::chunk {background-color: #00ABE4; }")
        # Explicitly redraw the widgets
        self.ui.plotWidget1.repaint()
        self.ui.plotWidget2.repaint()
        self.ui.lcdGesamtzahl.repaint()
        self.ui.lcdTemp.repaint()
        self.ui.LuftProgessBar.repaint()
        self.ui.lcdLuft.repaint()
         # Explizit neuzzeichnen
        self.ui.plotWidget1.repaint()
        self.ui.plotWidget2.repaint()

        print("Data plotted successfully")

    def onTabChanged(self, index):
        # Deaktiviere Mausereignisse für das nicht sichtbare Widget
        if index == 0:  # Tab 1 ist aktiv
            self.ui.plotWidget2.setMouseTracking(False)
            self.ui.plotWidget1.setMouseTracking(True)
        elif index == 1:  # Tab 2 ist aktiv
            self.ui.plotWidget1.setMouseTracking(False)
            self.ui.plotWidget2.setMouseTracking(True)

    def onMouseMoved(self, evt):
        pos = evt
        # Überprüfe, welcher Tab aktiv ist und leite das Ereignis an das entsprechende Plot-Widget weiter
        if self.ui.tabWidget.currentIndex() == 0:  # plotWidget1 aktiv
            if self.ui.plotWidget1.sceneBoundingRect().contains(pos):
                
                mousePoint = self.ui.plotWidget1.getViewBox().mapSceneToView(pos)
                index = int(mousePoint.x())
                y_value = int(mousePoint.y())
                if index >= 0 and index < len(self.zeiten):
                    self.ui.statusbar.showMessage(f'DATUM: {self.zeiten[int(mousePoint.x())]},  WERT: {mousePoint.y()}')
        elif self.ui.tabWidget.currentIndex() == 1:  # plotWidget2 aktiv
            if self.ui.plotWidget2.sceneBoundingRect().contains(pos):
                
                mousePoint = self.ui.plotWidget2.getViewBox().mapSceneToView(pos)
                index = int(mousePoint.x())
                y_value = int(mousePoint.y())
                if index >= 0 and index < len(self.zeiten):
                    self.ui.statusbar.showMessage(f'DATUM: {self.zeiten[index]}, Temperatur: {self.yTemp[y_value]:.2f}, Luftfeuchtigkeit: {self.yLuft[y_value]}')
                
           

    def process_data(self, data, sc_factor: scalefactor):
        yeinDaten = []
        yausDaten = []
        yanzMäuser = []
        zeiten = []
        yTemperature = []
        yLuft_F = []
        gesamtzahl = 0
        Temp = 0
        LuftFeuchtigkeit = 0

        daten = timescaling(data, sc_factor)
        if not daten:
            return zeiten, yeinDaten, yausDaten, yanzMäuser,yTemperature,yLuft_F ,gesamtzahl, LuftFeuchtigkeit, Temp

        match sc_factor:
            case scalefactor.Normal:
                last_line = daten[-1].split(",")
                if len(last_line) >= 6:
                    gesamtzahl = int(last_line[3].strip().replace("$", ""))
                    LuftFeuchtigkeit = float(last_line[4].strip().replace("%", ""))
                    Temp = float(last_line[5].strip().replace("C", ""))
                for line in daten:
                    verkehr = line.split(",")
                    if len(verkehr) >= 6:
                        zeit = verkehr[0]
                        yein = int(verkehr[1].strip().replace("->", ""))
                        yaus = int(verkehr[2].strip().replace("<-", ""))
                        yanz = int(verkehr[3].strip().replace("$", ""))
                        y_temp = float(verkehr[5].strip().replace("C", ""))
                        y_luft = float(verkehr[4].strip().replace("%", ""))

                        zeiten.append(zeit)
                        yeinDaten.append(yein)
                        yausDaten.append(yaus)
                        yanzMäuser.append(yanz)
                        yTemperature.append(y_temp)
                        yLuft_F.append(y_luft)

            case scalefactor.Day | scalefactor.Month:
                zeiten, yeinDaten, yausDaten, yanzMäuser, yTemperature, yLuft_F = process_average_data(daten)
                
                # Sort dates to get the most recent one
                sorted_dates = sorted(daten.keys())
                most_recent_date = sorted_dates[-1]
                last_values = daten[most_recent_date]
                
                the_last_value = last_values[-1]
                gesamtzahl = int(the_last_value[3].strip().replace("$", ""))
                LuftFeuchtigkeit = float(the_last_value[4].strip().replace("%", ""))
                Temp = float(the_last_value[5].strip().replace("C", ""))

            case _:
                return [], [], [], [], 0, 0, 0

        return zeiten, yeinDaten, yausDaten, yanzMäuser,yTemperature,yLuft_F ,gesamtzahl, LuftFeuchtigkeit, Temp

    def data_in_excel_speichern(self):

        # Erstellen eines QDialog
        dialog = QDialog()
        dialog.setWindowTitle("Daten in Excel Datei speichern")

          # Load and apply the stylesheet
        with open('style.qss', 'r') as file:
            dialog.setStyleSheet(file.read())
    
        # Layout und Widgets für den Dialog
        layout = QVBoxLayout()
        message1 = QLabel("Von: dd.mm.yy")
        layout.addWidget(message1)
        first_date = QDateEdit()
        first_date.setCalendarPopup(True)
        layout.addWidget(first_date)
        message2 = QLabel("Bis: dd.mm.yy")
        layout.addWidget(message2)
        last_date = QDateEdit()
        last_date.setCalendarPopup(True)
        layout.addWidget(last_date)
        
        # Hinzufügen von OK und Cancel Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: data_lesen_zeitraum(self.output_file,first_date, last_date, dialog))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.setLayout(layout)

        # Anzeigen des Dialogs
        if dialog.exec() == QDialog.Accepted:
            print("Dialog akzeptiert")
        else:
            print("Dialog abgelehnt")

    def clear_text_file(self):
        """Löscht den gesamten Inhalt einer Textdatei."""
        file_path = self.output_file
        dialog = QDialog
        try:
            with open(file_path, 'w') as file:
                file.truncate(0)  # Dateiinhalt auf 0 Bytes reduzieren
                file.close()
            print(f"Der Inhalt der Datei '{file_path}' wurde erfolgreich gelöscht.")
            QMessageBox.information(self, "Erfolg", f"die Backups Daten wurden erfolgreich '{file_path}' gelöscht")
            dialog.accept()
        except Exception as e:
            print(f"Fehler beim Löschen des Inhalts der Datei: {e}") 



    def monitor_serial_ports(self):
        while True:
            time.sleep(5)  # Überprüfe alle 5 Sekunden
            if not self.ser1 :
                self.show_warning("Serial Port Error", f"Serial port {self.serial_port1} is not available.")
                self.ser1 = None
            if not self.ser2 :
                self.show_warning("Serial Port Error", f"Serial port {self.serial_port2} is not available.")
                self.ser2 = None        

    def show_warning(self, title, message):
        QMessageBox.warning(self, title, message)

    def closeEvent(self, event):
        self.file_watcher.stop()
        event.accept()

    def start_file_writer(self):
         if True:  # Hier deine Bedingung für die seriellen Ports
            # Erstelle den Worker und den Thread
            self.worker = FileWriterWorker(self.serial_port1, self.serial_port2, self.ser1, self.ser2, self.output_file)
            self.thread = QThread()

            # Verbinde Worker mit dem Thread
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            # Starte den Thread
            self.thread.start()
            print("File writer started in background thread.")
             # Verbinde das Signal mit einem Slot, um die Nachricht anzuzeigen
            self.worker.finished.connect(self.show_message)

    def show_message(self):
        # Zeigt eine Nachricht an, wenn das Signal gesendet wird
        with open('style.qss', 'r') as file:
            self.setStyleSheet(file.read())
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Ein Microcontroller wurde getrennt \nVerbindung überprüfen und das Programm neu starten !")
        msg.setWindowTitle("Arduino Getrennt")
        msg.exec()
            

    def toggle_sidebar(self):
        if self.sidebar_open:
            # Sidebar ausblenden
            self.animation.setStartValue(QRect(self.x(), self.y(), self.width(), self.height()))
            self.animation.setEndValue(QRect(self.x() - self.width(), self.y(), self.width(), self.height()))
            self.sidebar_open = False
        else:
            # Sidebar einblenden
            self.animation.setStartValue(QRect(self.x() - self.width(), self.y(), self.width(), self.height()))
            self.animation.setEndValue(QRect(self.x(), self.y(), self.width(), self.height()))
            self.sidebar_open = True

        self.animation.start()

   
      

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Erstellen und Anzeigen des Video-Splash-Screens
    splash = VideoSplashScreen("0728.mp4")
    
    # Überprüfen, ob der Splash-Screen korrekt beendet wurde
    if splash.exec() == QDialog.Accepted:
        # Zeige das Hauptfenster nach dem Splash-Screen
        main_window = MainWindow()
        main_window.show()

        # Starte den Hintergrund-Worker für file_writer
        main_window.start_file_writer()

    # Beende die Anwendung korrekt
    sys.exit(app.exec())
