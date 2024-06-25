from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QLCDNumber
from PySide6.QtGui import QPixmap, QActionGroup
from mainwindow import Ui_MainWindow  # Assuming this is your UI file
from Taskhelper import timescaling, getAverage, data_lesen, scalefactor, Eigenschaften, process_average_data
import sys
import numpy as np
import matplotlib.pyplot as plt

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set segment style of QLCDNumber widget
        self.ui.lcdGesamtzahl.setSegmentStyle(QLCDNumber.Flat)

        self.data = None
        self.yeinDaten = None
        self.yausDaten = None
        self.zeiten = None
        self.gesamtzahl = 0
        self.LuftFeuchtigkeit = 0
        self.Temp = 0


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

        # Connect plot button with plot_data method
        self.ui.plotButton.clicked.connect(self.plot_data)
    
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

    def plot_data(self):
        self.data = data_lesen()
        if not self.data:
            return
        self.zeiten, self.yeinDaten, self.yausDaten,  self.yanzMäuser, gesamtzahl, LuftFeuchtigkeit, Temp = self.process_data(self.data, self.get_action_checked())

        # Get size of QGraphicsView
        view_size = self.ui.graphicsView.size()
        width, height = view_size.width(), view_size.height()

        # Plot data with Matplotlib and dynamically adjust size
        fig, ax = plt.subplots(figsize=(width / 90, height / 90))
        ax.plot(self.zeiten, self.yeinDaten, label='Einfluege', color='green')
        ax.plot(self.zeiten, self.yausDaten, label='Ausfluege', color='red')
        ax.plot(self.zeiten, self.yanzMäuser, label='Anz Fledermausern', color='skyblue')
        ax.set_xlabel('Zeit')
        ax.set_ylabel('Werte')
        ax.set_title('Ein- und Aus-Fluege über die Zeit')
        ax.legend()

        # Save plot to an image
        plt.savefig("plot.png", bbox_inches='tight', pad_inches=0)
        plt.close(fig)

        # Load image into QPixmap
        pixmap = QPixmap("plot.png")

        # Create a QGraphicsScene and add the image
        scene = QGraphicsScene()
        scene.addPixmap(pixmap)

        # Display the scene in the QGraphicsView
        self.ui.graphicsView.setScene(scene)

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
            return  zeiten, yeinDaten, yausDaten, yanzMäuser, gesamtzahl
        

      
        # if len(last_values) >= 4:
        #     gesamtzahl = int(last_values[3].strip().replace("$", ""))
        # if len(last_values) >= 6:
        #     LuftFeuchtigkeit = float(last_values[4].strip().replace("%", ""))
        #     Temp = float(last_values[5].strip().replace("C", ""))
        match sc_factor:
            case scalefactor.Normal:
                last_line = daten[-1].split(",")
                if len(last_line) >= 6:
                    gesamtzahl = int(last_line[3].strip().replace("$",""))
                    LuftFeuchtigkeit = float(last_line[4].strip().replace("%",""))
                    Temp = float(last_line[5].strip().replace("C",""))
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
                gesamtzahl = int(the_last_value[3].strip().replace("$",""))
                LuftFeuchtigkeit = float(the_last_value[4].strip().replace("%",""))
                Temp = float(the_last_value[5].strip().replace("C","") )


            case _:
                return [], [], [], [], 0, 0, 0

        return  zeiten, yeinDaten, yausDaten, yanzMäuser, gesamtzahl, LuftFeuchtigkeit, Temp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

