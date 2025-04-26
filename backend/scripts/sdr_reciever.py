"""
Adapted from Code Metal SDR examples.
Listens on SDR, decodes text alerts, and POSTs to /alerts.
"""
import requests
import subprocess
import json

API_URL = "http://localhost:8000/alerts"
SDR_CMD = ["python3", "sdr_decode.py"]  # replace with actual decode command

def run_receiver():
    proc = subprocess.Popen(SDR_CMD, stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:
        alert_text = line.strip()
        # expect format "TYPE at lat,lon"
        try:
            parts = alert_text.split(" at ")
            typ = parts[0]
            coords = parts[1].split(",")
            payload = {
                "type": typ,
                "location": [float(coords[0]), float(coords[1])],
                "units_responding": 1
            }
            resp = requests.post(API_URL, json=payload)
            print(f"Posted SDR alert: {payload}, status: {resp.status_code}")
        except Exception as e:
            print("Received non-alert or failed parse:", alert_text, e)

if __name__ == "__main__":
    run_receiver()
