# 🌿 Plant Monitoring System

A complete IoT-based system for real-time plant monitoring using an Arduino and a Raspberry Pi. The system collects temperature, humidity, soil moisture, pH, and light intensity data from sensors, streams it to a Raspberry Pi, and displays everything on a live web dashboard with integrated camera feed.

## 📦 Project Structure

```

plant-monitoring-system/
│
├── arduino/               # Arduino code for sensor collection and fan control
├── raspberrypi/           # Flask app for data visualization and video streaming
│   ├── templates/         # HTML template for the web dashboard
│   └── cnn/               # Reserved for future ML integration
├── captureTest.py         # Test script for USB camera capture
├── usb\_streamer.py        # USB camera streaming utility
├── video\_streamer.py      # Alternate or legacy video streaming script
├── README.md              # You're here!
└── .gitignore             # Ignore rules

````

## 🛠 Features

- 🌡 Real-time temperature, humidity, pH, light, and soil moisture monitoring
- 📟 LCD display on Arduino side
- 💨 Automatic fan control based on temperature
- 🔗 Serial communication from Arduino to Raspberry Pi
- 📈 Live web dashboard using Flask and Socket.IO
- 📷 USB camera live feed integration

## 🚀 Getting Started

### 1. Arduino

- Upload the code in `arduino/` to your Arduino board
- Connect the sensors and LCD as specified in the code

### 2. Raspberry Pi

- Install Python dependencies:
  ```bash
  pip install flask flask-socketio eventlet pyserial opencv-python

* Run the Flask app:

  ```bash
  python raspberrypi/app.py
  ```
* Access the dashboard via:

  ```
  http://<your-pi-ip>:5000
  ```

## 👨‍💻 Author

* **Bakel Bakel** – [GitHub](https://github.com/Bakel-Bakel)

