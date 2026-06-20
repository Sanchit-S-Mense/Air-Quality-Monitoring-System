import serial
import csv
import time
from datetime import datetime


def unpackData(data):
    # Splits the string and converts to floats
    temp, humidity, aq = data.split(",")
    return float(temp), float(humidity), float(aq)


arduino_port = "/dev/cu.usbserial-1130"
baud_rate = 9600

# ERROR HANDLING 1: Catch Connection Issues
try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    time.sleep(2)  # Give Arduino a moment to reset
    print(f"Successfully connected to {arduino_port}")
except serial.SerialException as e:
    print(f"CRITICAL ERROR: Could not connect to {arduino_port}.")
    print("Check if the Arduino is plugged in and the port name is correct.")
    print(f"System Error Message: {e}")
    exit()  # Stop the script entirely, as we can't do anything without the hardware

# Create and open a CSV file
today = datetime.now()
formatted_date = today.strftime("%d-%m-%Y")

with open(f'{formatted_date}_sensor_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    headers = ["Time", "Temperature", "Humidity", "AQ"]
    writer.writerow(headers)

    print("Listening to Arduino... Press Ctrl+C to stop.")

    try:
        while True:
            if ser.in_waiting > 0:
                # Read the line, decode, and strip whitespace
                line = ser.readline().decode('utf-8').rstrip()

                # Ignore blank lines to prevent crashes
                if not line:
                    continue
                # Format current time
                current_time = datetime.now().strftime('%H:%M:%S')
                print(f"Data received at {current_time}: {line}")  # Helpful for debugging

                # ERROR HANDLING 2: Catch Malformed Data
                try:
                    # Attempt to unpack the data
                    temp, humidity, aq = unpackData(line)

                    # LOGICAL FIX: Write a single row as a list
                    writer.writerow([current_time, temp, humidity, aq])

                    # Pro-tip: Force the file to save immediately.
                    # Without this, if your computer crashes, you lose the data!
                    file.flush()

                except ValueError as e:
                    # If split() fails (missing commas) or float() fails (letters instead of numbers)
                    print(f"WARNING: Received bad data, skipping this line. Data was: '{line}'")

    except KeyboardInterrupt:
        # User pressed Ctrl+C
        print("\nData logging stopped safely by user.")

    finally:
        # ERROR HANDLING 3: Always cleanly close the port when the script ends
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")