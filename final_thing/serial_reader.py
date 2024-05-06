import csv
import pyserial as serial

port = 'COM3'
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
            data = line.split(',')  # Split the line into a list (replace ',' with your delimiter)
            writer.writerow(data)  # Write the data to the CSV file
