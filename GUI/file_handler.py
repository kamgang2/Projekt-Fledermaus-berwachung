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