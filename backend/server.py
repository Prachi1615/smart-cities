from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import uvicorn

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# —— Data Models ——
class Alert(BaseModel):
    type: str
    location: list[float]
    units_responding: int
    priority: str = "High"
    drone_id: str | None = None

class SensorData(BaseModel):
    temperature: float
    smoke_level: float
    humidity: float

class DronePosition(BaseModel):
    id: str
    lat: float
    lon: float
    altitude: float

class Obstacle(BaseModel):
    type: str
    location: list[float]

class ActionReport(BaseModel):
    report: str

class SensorSite(BaseModel):
    site_id: int
    location: list[float]

# —— In-memory stores ——
alerts: list[Alert]            = []
sensors: SensorData | None     = None
drones: list[DronePosition]    = []
obstacles: list[Obstacle]      = []
action_reports: list[ActionReport] = []
sensor_sites: list[SensorSite] = []

# —— Endpoints —— 

# Alerts
@app.get("/alerts")
def get_alerts():
    return alerts

@app.post("/alerts")
def post_alert(alert: Alert):
    alerts.append(alert)
    return {"status": "ok"}

# Sensors
@app.get("/sensors")
def get_sensors():
    if sensors:
        return sensors
    return {
        "temperature": random.uniform(60, 150),
        "smoke_level": random.uniform(0, 100),
        "humidity": random.uniform(20, 80),
    }

@app.post("/sensors")
def post_sensors(data: SensorData):
    global sensors
    sensors = data
    return {"status": "ok"}

# Units (static example)
@app.get("/units")
def get_units():
    return [
        {"id": "Unit 42", "status": "Available"},
        {"id": "Unit 17", "status": "On Scene"},
    ]

# Drones
@app.get("/drones")
def get_drones():
    return drones

@app.post("/drones")
def post_drone(pos: DronePosition):
    # update or append by id
    for i, d in enumerate(drones):
        if d.id == pos.id:
            drones[i] = pos
            break
    else:
        drones.append(pos)
    return {"status": "ok"}

# Cameras (static example)
@app.get("/cameras")
def get_cameras():
    return [
        {"name": "Street Cam 01", "url": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4"}
    ]

# Obstacles
@app.get("/obstacles")
def get_obstacles():
    return obstacles

@app.post("/obstacles")
def post_obstacle(obs: Obstacle):
    obstacles.append(obs)
    return {"status": "ok"}

# Action Reports
@app.get("/action_reports")
def get_action_reports():
    return action_reports

@app.post("/action_reports")
def post_action_report(report: ActionReport):
    action_reports.append(report)
    return {"status": "ok"}

# Sensor Site Placements
@app.get("/sensor_sites")
def get_sensor_sites():
    return sensor_sites

@app.post("/sensor_sites")
def post_sensor_site(site: SensorSite):
    sensor_sites.append(site)
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
