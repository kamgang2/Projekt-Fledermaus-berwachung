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



# Open the file to write the data
with open(output_file, 'a') as file:
    try:
        while True:
            if ser1.in_waiting > 0 and ser2.in_waiting > 0:
                # Read a line from the serial port
                line1 = ser1.readline().decode('utf-8').strip() 
                line2 = ser2.readline().decode('utf-8').strip()
                timestamp = datetime.datetime.now()
                # Print the line to the console
                myDataLine =timestamp.strftime("%d-%m-%Y %H:%M:%S")+","+ line1 +","+ line2
                print(myDataLine)
                # Write the line to the file
                file.write(myDataLine + '\n')
            else:
                print("No data waiting in the serial buffer.")
            time.sleep(1)  # Add a small delay to prevent high CPU usage
    except KeyboardInterrupt:
        print("Program interrupted. Closing...")
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
    finally:
        ser1.close()
        print(f"Disconnected from {serial_port1}.")






    