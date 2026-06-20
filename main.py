import serial
import csv
import time

# 1. Setup the Serial port (Change 'COM3' to whatever your Arduino uses! On Mac it might be '/dev/cu.usbmodem14101')
arduino_port = '/dev/cu.usbserial-130'
baud_rate = 9600  # Make sure this matches your Arduino code

# 2. Open the serial connection
ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)  # Give Arduino a moment to reset

# 3. Create and open a CSV file to write the data
with open('live_sensor_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Raw Output'])  # Header

    print("Listening to Arduino... Press Ctrl+C to stop.")

    try:
        while True:
            if ser.in_waiting > 0:
                # Read the line from Arduino, decode it, and strip whitespace
                line = ser.readline().decode('utf-8').rstrip()


                # Write it to the CSV
                if line.isnumeric():
                    # Print to terminal so you can see it
                    print(line)
                    writer.writerow([line])

    except KeyboardInterrupt:
        print("Data logging stopped.")
        ser.close()