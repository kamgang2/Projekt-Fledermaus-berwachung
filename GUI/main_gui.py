from PySide6.QtWidgets import QApplication, QMainWindow, QLCDNumber, QSpinBox, QDialog, QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QDateEdit, QMessageBox
from PySide6.QtGui import QPixmap, QActionGroup, QColor, QFontDatabase, QFont, QIcon
from mainwindow import Ui_MainWindow  
from Taskhelper import timescaling, scalefactor, process_average_data, convert_to_datetime, SpinBoxDialog,FileWatcher, SerialMonitorThread
from file_handler import file_writter, data_lesen, data_lesen_zeitraum
from splashscreen import VideoSplashScreen
import sys
import pyqtgraph as pg
from PySide6.QtCore import Qt, Slot
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
        self.serial_port2 = 'COM5'
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
            self.ser1 = None
            self.ser2 = None
            

        self.ui.setupUi(self)

        # # Hintergrundfarbe als hexadezimale Zeichenkette
        # hex_color = "#E9F1FA"

        # # # Konvertieren Sie die hexadezimale Zeichenkette in ein QColor-Objekt
        # color = QColor(hex_color)
        self.ui.plotWidget1.setBackground('w')
        self.ui.plotWidget2.setBackground('w')

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

        # Connect plot button with plot_data method
        self.plot_data()

        self.file_watcher = FileWatcher(os.path.join(os.path.dirname(__file__),  self.output_file))
        self.file_watcher.start()
        self.file_watcher.file_modified.connect(self.on_file_modified)
        
        self.start_file_writer()

        # Create and start the QThread for monitoring serial ports
        self.monitor_thread = SerialMonitorThread(self.serial_port1, self.serial_port2, self.ser1, self.ser2)
        self.monitor_thread.warning_signal.connect(self.show_warning)
        self.monitor_thread.start()

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

        print("Data plotted successfully")

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

    def show_warning(self, title, message):
        QMessageBox.warning(self, title, message)

    def closeEvent(self, event):
        self.file_watcher.stop()
        event.accept()

    def start_file_writer(self):
        if self.ser1 and self.ser2:
            # Thread for file writing
            print("Thread for file_writer")
            thread_file_writer = threading.Thread(
                target=file_writter,
                args=(self.serial_port1, self.serial_port2, self.ser1, self.ser2, self.output_file),
                daemon=True
            )
            thread_file_writer.start()
      

if __name__ == "__main__":
    app = QApplication(sys.argv)
     # Create and show the video splash screen
    splash = VideoSplashScreen("0728.mp4")
    if splash.exec() == QDialog.Accepted:
        # Show the main window after the splash screen
        main_window = MainWindow()
        main_window.show()

    sys.exit(app.exec())
