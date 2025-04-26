from datetime import datetime
import psutil
import csv
import os

# Path to save CSV
CSV_FILE = "battery_log.csv"

def log_battery_status():
    battery = psutil.sensors_battery()
    percent = battery.percent
    plugged = battery.power_plugged
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if file already exists
    file_exists = os.path.isfile(CSV_FILE)

    # Open the CSV file and append a new row
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)

        # If the file didn't exist, write headers first
        if not file_exists:
            writer.writerow(["timestamp", "percent", "plugged"])

        writer.writerow([timestamp, percent, plugged])