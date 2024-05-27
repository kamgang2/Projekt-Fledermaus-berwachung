import serial  # install with " pip3 install pyserial"
import time

# Configure the serial port and the baud rate
serial_port = 'COM4'  # Replace with your serial port
baud_rate = 9600
output_file = 'serial_data.txt'

try:
    # Open the serial port
    ser = serial.Serial(serial_port, baud_rate)
    time.sleep(2)  # Wait for the serial connection to initialize
    print(f"Connected to {serial_port} at {baud_rate} baud.")
except serial.SerialException as e:
    print(f"Error opening serial port {serial_port}: {e}")
    exit(1)



# Open the file to write the data
with open(output_file, 'a') as file:
    try:
        while True:
            if ser.in_waiting > 0:
                # Read a line from the serial port
                line = ser.readline().decode('utf-8').strip() 
                # Print the line to the console
                print(line)
                # Write the line to the file
                file.write(line + '\n')
            else:
                print("No data waiting in the serial buffer.")
            time.sleep(1)  # Add a small delay to prevent high CPU usage
    except KeyboardInterrupt:
        print("Program interrupted. Closing...")
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
    finally:
        ser.close()
        print(f"Disconnected from {serial_port}.")
