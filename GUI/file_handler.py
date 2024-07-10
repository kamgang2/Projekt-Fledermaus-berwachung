import serial  # install with " pip3 install pyserial"
import time
import datetime
from openpyxl import workbook
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QDateEdit,QFileDialog, QMessageBox


def file_writter(serial_port1, serial_port2, ser1, ser2, output_file): 
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
                    timestamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
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
            print(f"Disconnected from {serial_port1} and {serial_port2}.")   



def data_lesen(lese_datei):
        # Öffnen der Datei im Lesemodus
        try:
            with open(lese_datei, "r") as myfile:
                # Initialisieren einer leeren Liste, um die Zeilen zu speichern
                lines = []
                
                # Durchlaufen jeder Zeile in der Datei
                for line in myfile:
                    # Entfernen des Zeilenumbruchs und Hinzufügen zur Liste
                    lines.append(line.strip())
                
                # Rückgabe der Liste mit den Zeilen
                return lines
        except FileNotFoundError:
            print(f"Datei {lese_datei} nicht gefunden.")
            return []
        

def data_in_excel_speichern(lese_datei): 
    # Erstellen eines QDialog
    dialog = QDialog()
    dialog.setWindowTitle("Daten in Excel Datei speichern")
   
    # Layout und Widgets für den Dialog
    layout = QVBoxLayout()
    message1 = QLabel("Von: DD.MM.YY")
    layout.addWidget(message1)
    first_date = QDateEdit()
    first_date.setCalendarPopup(True)
    layout.addWidget(first_date)
    message2 = QLabel("Bis: DD.MM.YY")
    layout.addWidget(message2)
    last_date = QDateEdit()
    last_date.setCalendarPopup(True)
    layout.addWidget(last_date)
    
    # Hinzufügen von OK und Cancel Buttons
    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    buttons.accepted.connect(lambda: data_lesen_zeitraum(lese_datei,first_date, last_date, dialog))
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)

    dialog.setLayout(layout)

    # Anzeigen des Dialogs
    if dialog.exec() == QDialog.Accepted:
        print("Dialog akzeptiert")
    else:
        print("Dialog abgelehnt")


def data_lesen_zeitraum(lese_datei,date1, date2, dialog):
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getSaveFileName(dialog, "Speichern unter", "", "Excel Dateien (*.xlsx);;Alle Dateien (*)", options=options)
    
    if file_path:
        try:
            data_fromTo = []  
            myData = data_lesen(lese_datei)  # Assuming data_lesen is a method in your class
            for line in myData: 
                line_splited = line.split(",")
                line_date = datetime.strptime(line_splited[0].split(" ")[0], "%d.%m.%Y").date()
                if date1 <= line_date <= date2:
                    data_fromTo.append(line_splited)

            wb = workbook()
            ws = wb.active

            ws.append(['Datum', 'Einfluege', 'Ausfluege', 'Anz der Fledermause', 'Luftfeuchtigkeit', 'Temperature'])
            for line in data_fromTo:
                ws.append(line)

            wb.save(file_path)
            QMessageBox.information(dialog, "Erfolg", f"Daten erfolgreich in '{file_path}' gespeichert")
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(dialog, "Fehler", f"Fehler beim Speichern der Datei: {e}")
            dialog.reject()



