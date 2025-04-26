"""
backend/scripts/obstacle_detector.py

Simulate or detect obstacles (roadblocks, debris, fires) and POST them to /obstacles.
"""
import time
import random
import requests

API_URL = "http://localhost:8000/obstacles"

def stream_obstacles():
    while True:
        obs = {
            "type": random.choice(["Roadblock", "Debris", "Fire"]),
            "location": [
                37.7749 + random.uniform(-0.005, 0.005),
                -122.4194 + random.uniform(-0.005, 0.005)
            ]
        }
        try:
            r = requests.post(API_URL, json=obs)
            print(f"Posted obstacle {obs} → {r.status_code}")
        except Exception as e:
            print("Error posting obstacle:", e)
        time.sleep(15)  # adjust as needed

if __name__ == "__main__":
    stream_obstacles()
