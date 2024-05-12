"""Reads from serial port and writes to a CSV file."""
import csv
import serial

PORT = 'COM5'
BAUDRATE = 115200
OUT_FILENAME = 'output.csv'
# Open the serial port (replace '/dev/ttyUSB0' with your port path)
ser = serial.Serial(port=PORT, baudrate=BAUDRATE)

# Open (or create) the CSV file for writing
with open(file=OUT_FILENAME, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(csvfile=file)

    # Read from the serial port
    while True:
        # Read a line from the serial port
        line: str = ser.readline().decode(encoding='utf-8').strip()
        if line:
            # Split the line into a list
            timestamp, spl= line.split(sep=';')
            print(f"time: {timestamp}, SPL: {spl}")
            # Write the data to the CSV file
            writer.writerow([timestamp,spl])
