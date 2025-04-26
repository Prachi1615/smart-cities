# backend/scripts/dedrone_uploader.py

"""
Parses Dedrone DJI positional CSV (Site1_DJI_Data.csv) and POSTs positions to /drones.
"""

import time
import csv
import requests
import os

# URL of your backend drones endpoint
API_URL = "http://localhost:8000/drones"

# Path to your Dedrone positional data CSV
CSV_FILE = os.path.join(
    os.path.dirname(__file__),
    os.pardir,
    "dedrone-data",
    "Site1_DJI_Data.csv"
)

def upload_drone_positions():
    while True:
        try:
            with open(CSV_FILE, newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # adjust these keys if your CSV uses different column names
                    drone_id = row.get("drone_id") \
                               or row.get("DeviceID") \
                               or row.get("Device_Address") \
                               or row.get("id")
                    latitude  = float(row["Latitude"])
                    longitude = float(row["Longitude"])
                    altitude  = float(row.get("Altitude", 0))

                    payload = {
                        "id": str(drone_id),
                        "lat": latitude,
                        "lon": longitude,
                        "altitude": altitude
                    }
                    resp = requests.post(API_URL, json=payload)
                    print(f"Posted drone {drone_id}: ({latitude}, {longitude}, {altitude}) → {resp.status_code}")
        except Exception as e:
            print("Error reading or posting Dedrone data:", e)

        # pause before the next batch
        time.sleep(5)

if __name__ == "__main__":
    upload_drone_positions()
