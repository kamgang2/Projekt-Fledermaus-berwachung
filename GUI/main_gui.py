from PySide6.QtWidgets import QApplication, QMainWindow, QLCDNumber, QSpinBox, QDialog
from PySide6.QtGui import QPixmap, QActionGroup
from mainwindow import Ui_MainWindow  
from Taskhelper import timescaling, getAverage, data_lesen, scalefactor, Eigenschaften, process_average_data, convert_to_datetime, SpinBoxDialog,FileWatcher
import sys
import pyqtgraph as pg
from PySide6.QtCore import Qt, Slot
import serial
import os


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
        self.ui.setupUi(self)
        self.ui.plotWidget1.setBackground('w')
        self.ui.plotWidget2.setBackground('w')

        # Set segment style of QLCDNumber widget
        self.ui.lcdGesamtzahl.setSegmentStyle(QLCDNumber.Flat)

        self.data = None
        self.yeinDaten = None
        self.yausDaten = None
        self.zeiten = None
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

        # Connect plot button with plot_data method
        self.plot_data()

        self.file_watcher = FileWatcher(os.path.join(os.path.dirname(__file__), "serial_data.txt"))
        self.file_watcher.file_modified.connect(self.on_file_modified)
        self.file_watcher.start()

    def show_spinbox_dialog(self):
        if self.spinbox_dialog.exec() == QDialog.Accepted:
            value = self.spinbox_dialog.get_value()
            self.set_anz_fledermause(value)
            self.repaint()
    
    def set_anz_fledermause(self, value):
        upload_port = "COM4"
        baud_rate = 9600
        with serial.Serial(upload_port, baud_rate) as serial_monitor:
            serial_monitor.write(f"startwert_fleder: {value}".encode())

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
        self.data = data_lesen()
        if not self.data:
            return
        self.zeiten, self.yeinDaten, self.yausDaten, self.yanzMäuser, gesamtzahl, LuftFeuchtigkeit, Temp = self.process_data(self.data, self.get_action_checked())

        # Convert times to datetime
        self.zeiten = [convert_to_datetime(x) for x in self.zeiten]

        # Create a mapping from time to index for custom axis labels
        time_to_index = {t: i for i, t in enumerate(self.zeiten)}
        indices = [time_to_index[t] for t in self.zeiten]

        self.ui.plotWidget1.clear()
        self.ui.plotWidget1.addLegend()

        # Define pens with different thickness
        pen_ein = {'color': 'g', 'width': 3}  # Thickness for 'Einfluege'
        pen_aus = {'color': 'r', 'width': 3}  # Thickness for 'Ausfluege'
        pen_anz = {'color': 'b', 'width': 3}  # Thickness for 'Anz Fledermaeuser'

        self.ui.plotWidget1.plot(indices, self.yeinDaten, pen=pen_ein, name='Einfluege')
        self.ui.plotWidget1.plot(indices, self.yausDaten, pen=pen_aus, name='Ausfluege')
        self.ui.plotWidget1.plot(indices, self.yanzMäuser, pen=pen_anz, name='Anz Fledermaeuser')

        # Set labels and title
        self.ui.plotWidget1.setLabel('left', 'Werte')
        self.ui.plotWidget1.setLabel('bottom', 'Zeit')
        self.ui.plotWidget1.setTitle('Ein- und Aus-Fluege über die Zeit')

        # Use CustomAxisItem to correctly display custom labels on the x-axis
        date_labels = {i: str(t) for i, t in enumerate(self.zeiten)}
        custom_axis = CustomAxisItem(labels=date_labels, orientation='bottom')
        self.ui.plotWidget1.setAxisItems({'bottom': custom_axis})

        # Display total count
        self.ui.lcdGesamtzahl.display(gesamtzahl)

        # Display temperature
        self.ui.lcdTemp.display(Temp)
        self.ui.TempProgessBar.setValue(Temp)
        if Temp < -5:
            self.ui.TempProgessBar.setStyleSheet("QProgressBar::chunk {background-color: blue; }")
        elif -5 <= Temp < 5:
            self.ui.TempProgessBar.setStyleSheet("QProgressBar::chunk {background-color: lightblue; }")
        elif 5 <= Temp < 25:
            self.ui.TempProgessBar.setStyleSheet("QProgressBar::chunk {background-color: green; }")
        elif 25 <= Temp < 35:
            self.ui.TempProgessBar.setStyleSheet("QProgressBar::chunk {background-color: yellow; }")
        else:
            self.ui.TempProgessBar.setStyleSheet("QProgressBar::chunk {background-color: red; }")

        # Display humidity
        self.ui.lcdLuft.display(LuftFeuchtigkeit)

        # Explicitly redraw the widgets
        self.ui.plotWidget1.repaint()
        self.ui.lcdGesamtzahl.repaint()
        self.ui.lcdTemp.repaint()
        self.ui.TempProgessBar.repaint()
        self.ui.lcdLuft.repaint()

        print("Data plotted successfully")

    def process_data(self, data, sc_factor: scalefactor):
        yeinDaten = []
        yausDaten = []
        yanzMäuser = []
        zeiten = []
        gesamtzahl = 0
        Temp = 0
        LuftFeuchtigkeit = 0

        daten = timescaling(data, sc_factor)
        if not daten:
            return zeiten, yeinDaten, yausDaten, yanzMäuser, gesamtzahl, LuftFeuchtigkeit, Temp

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

                        zeiten.append(zeit)
                        yeinDaten.append(yein)
                        yausDaten.append(yaus)
                        yanzMäuser.append(yanz)

            case scalefactor.Day | scalefactor.Month:
                zeiten, yeinDaten, yausDaten, yanzMäuser = process_average_data(daten)
                
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

        return zeiten, yeinDaten, yausDaten, yanzMäuser, gesamtzahl, LuftFeuchtigkeit, Temp

    def closeEvent(self, event):
        self.file_watcher.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())