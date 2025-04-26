"""
Adapted from Code Metal IoT examples.
Continuously reads (simulated) sensor data and POSTs to /sensors.
"""
import time
import requests
import random

API_URL = "http://localhost:8000/sensors"

def stream_sensor_data():
    while True:
        data = {
            "temperature": round(random.uniform(60, 150), 2),
            "smoke_level": round(random.uniform(0, 100), 2),
            "humidity": round(random.uniform(20, 80), 2)
        }
        try:
            resp = requests.post(API_URL, json=data)
            print(f"Posted sensors: {data}, status: {resp.status_code}")
        except Exception as e:
            print("Error posting sensors:", e)
        time.sleep(10)  # every 10s

if __name__ == "__main__":
    stream_sensor_data()
