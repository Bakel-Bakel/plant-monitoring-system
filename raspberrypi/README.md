# Raspberry Pi Flask App

This folder contains the Flask-based backend and frontend used to read serial data from Arduino and visualize it in a web dashboard.

## 📂 Contents

- `app.py` – Main Flask + SocketIO server
- `plant.service` – systemd service file to autostart on boot
- `templates/index.html` – Frontend dashboard HTML
- `cnn/` – Placeholder for machine learning models

## 🚀 Features

- Real-time serial data reading from Arduino
- Live camera feed from USB camera
- WebSocket-based dashboard updates (no page refresh)
- systemd-compatible with auto-start on boot

## 🔧 Setup

1. Connect Arduino to Pi via USB
2. Connect USB camera (shows as `/dev/video0`)
3. Install dependencies:
   ```bash
   pip install flask flask-socketio eventlet pyserial opencv-python
4. Run:

   ```python
   python app.py
   ```

Or enable as a service:

```bash
sudo cp plant.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable plantmonitor
sudo systemctl start plantmonitor
```

Then visit: `http://<your-pi-ip>:5000`

## ✅ Example Output

```text
[Sensor Readings]
Temperature: 24.5 °C
Humidity   : 62.3 %
pH Value   : 6.7
Soil Moist : 388
Light Lux  : 212.0
```



