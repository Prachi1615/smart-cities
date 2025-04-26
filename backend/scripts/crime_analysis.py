"""
backend/scripts/crime_analysis.py

Fetches SF Police incident reports from Socrata, clusters hotspots,
and POSTs ideal sensor‐site locations to /sensor_sites.
"""
import time
import requests
from sodapy import Socrata
from sklearn.cluster import KMeans

# Socrata client for SF Open Data
# You can register for an App Token if you exceed rate limits
client = Socrata("data.sfgov.org", None)

API_URL      = "http://localhost:8000/sensor_sites"
DATASET_ID   = "wg3w-h783"   # Police Department Incident Reports
CRIME_LIMIT  = 5000          # how many recent incidents to fetch
NUM_SITES    = 5             # number of sensor sites to compute

def fetch_crime_data():
    # Fetch the most recent incidents with latitude & longitude
    results = client.get(DATASET_ID,
                         select="latitude,longitude",
                         where="latitude IS NOT NULL AND longitude IS NOT NULL",
                         order="incident_datetime DESC",
                         limit=CRIME_LIMIT)
    # Convert into list of (lon, lat)
    coords = [(float(r["longitude"]), float(r["latitude"])) for r in results]
    return coords

def compute_sensor_sites():
    coords = fetch_crime_data()
    if len(coords) < NUM_SITES:
        print("Not enough data for clustering.")
        return
    # Cluster into NUM_SITES hotspots
    kmeans = KMeans(n_clusters=NUM_SITES, random_state=0).fit(coords)
    centers = kmeans.cluster_centers_

    # POST each center as a sensor site
    for idx, (lon, lat) in enumerate(centers, start=1):
        site = {"site_id": idx, "location": [lat, lon]}
        try:
            r = requests.post(API_URL, json=site)
            print(f"→ Posted site {idx}: {[lat,lon]} status={r.status_code}")
        except Exception as e:
            print("Error posting sensor site:", e)

if __name__ == "__main__":
    # Run once; you can also schedule this periodically
    compute_sensor_sites()
