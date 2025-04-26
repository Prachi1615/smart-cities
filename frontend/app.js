// Initialize map
const map = L.map('map').setView([37.7749, -122.4194], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Layers
const alertsLayer    = L.layerGroup().addTo(map);
const dronesLayer    = L.layerGroup().addTo(map);
const obstaclesLayer = L.layerGroup().addTo(map);
const sitesLayer     = L.layerGroup().addTo(map);

// Utility for priority color
function getColor(p) {
  return p === 'High'   ? 'red' :
         p === 'Medium' ? 'orange' :
         p === 'Low'    ? 'green' : 'blue';
}

// Fetch/update functions
async function updateSensors() {
  const { temperature, smoke_level, humidity } =
    await (await fetch('/sensors')).json();
  document.getElementById('temp').innerText      = temperature.toFixed(1);
  document.getElementById('smoke').innerText     = smoke_level.toFixed(1);
  document.getElementById('humidity').innerText  = humidity.toFixed(1);
}

async function updateUnits() {
  const units = await (await fetch('http://localhost:8000/units')).json();
  const el = document.getElementById('units');
  el.innerHTML = '';
  units.forEach(u => {
    const p = document.createElement('p');
    p.textContent = `${u.id}: ${u.status}`;
    el.appendChild(p);
  });
}

async function updateDrones() {
  const list = await (await fetch('http://localhost:8000/drones')).json();
  dronesLayer.clearLayers();
  const el = document.getElementById('drones');
  el.innerHTML = '';
  list.forEach(d => {
    L.marker([d.lat, d.lon]).addTo(dronesLayer)
      .bindPopup(`Drone ${d.id}<br>Alt: ${d.altitude}m`);
    const p = document.createElement('p');
    p.textContent = `${d.id}: [${d.lat.toFixed(4)}, ${d.lon.toFixed(4)}]`;
    el.appendChild(p);
  });
}

async function updateAlerts() {
  const list = await (await fetch('http://localhost:8000/alerts')).json();
  alertsLayer.clearLayers();
  list.forEach(a => {
    const color = getColor(a.priority);
    L.circle(a.location, {
      color, fillColor: color, fillOpacity: 0.5, radius: 100
    }).addTo(alertsLayer)
      .bindPopup(`${a.type}<br>Units: ${a.units_responding}`);
  });
}

async function updateCameras() {
  const cams = await (await fetch('http://localhost:8000/cameras')).json();
  const el = document.getElementById('cameras');
  el.innerHTML = '';
  cams.forEach(c => {
    const p = document.createElement('p');
    p.textContent = c.name;
    const iframe = document.createElement('iframe');
    iframe.src = c.url;
    el.appendChild(p);
    el.appendChild(iframe);
  });
}

async function updateObstacles() {
  const list = await (await fetch('http://localhost:8000/obstacles')).json();
  obstaclesLayer.clearLayers();
  const el = document.getElementById('obstacles');
  el.innerHTML = '';
  list.forEach(o => {
    L.circle(o.location, { color: 'gray', radius: 50 })
      .addTo(obstaclesLayer)
      .bindPopup(o.type);
    const li = document.createElement('li');
    li.textContent = `${o.type} @ [${o.location.map(n=>n.toFixed(4)).join(', ')}]`;
    el.appendChild(li);
  });
}

async function updateReports() {
  const list = await (await fetch('http://localhost:8000/action_reports')).json();
  const el = document.getElementById('reports');
  el.innerHTML = '';
  list.forEach(r => {
    const li = document.createElement('li');
    li.textContent = r.report;
    el.appendChild(li);
  });
}

async function updateSensorSites() {
  const list = await (await fetch('http://localhost:8000/sensor_sites')).json();
  sitesLayer.clearLayers();
  const el = document.getElementById('sensor-sites');
  el.innerHTML = '';
  list.forEach(s => {
    L.marker(s.location, {
      icon: L.icon({ iconUrl: 'sensor-icon.png', iconSize: [24,24] })
    }).addTo(sitesLayer)
      .bindPopup(`Site ${s.site_id}`);
    const li = document.createElement('li');
    li.textContent = `Site ${s.site_id}: [${s.location.map(n=>n.toFixed(4)).join(', ')}]`;
    el.appendChild(li);
  });
}

// Master refresh
async function refreshAll() {
  await Promise.all([
    updateSensors(),
    updateUnits(),
    updateDrones(),
    updateAlerts(),
    updateCameras(),
    updateObstacles(),
    updateReports(),
    updateSensorSites()
  ]);
}

// Run every 5s
setInterval(refreshAll, 5000);
refreshAll();
