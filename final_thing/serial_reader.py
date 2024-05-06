import csv
import serial

port = 'COM5'
baudrate = 115200
out_filename = 'output.csv'
# Open the serial port (replace '/dev/ttyUSB0' with your port path)
ser = serial.Serial(port, baudrate)

# Open (or create) the CSV file for writing
with open(out_filename, 'w', newline='') as file:
    writer = csv.writer(file)

    # Read from the serial port
    while True:
        line = ser.readline().decode('utf-8').strip()  # Read a line from the serial port
        if line:  # If the line is not empty
            timestamp, spl= line.split(';')  # Split the line into a list (replace ',' with your delimiter)
            print(f"time: {timestamp}, SPL: {spl}")
            writer.writerow([timestamp,spl])  # Write the data to the CSV file
