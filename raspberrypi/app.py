from flask import Flask, render_template
from flask_socketio import SocketIO
import serial
import threading

app = Flask(__name__)
socketio = SocketIO(app)

# Connect to Arduino serial
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust port if necessary

def read_from_arduino():
    while True:
        try:
            line = ser.readline().decode().strip()
            parts = line.split(',')
            if len(parts) == 5:
                data = {
                    'temperature': parts[0],
                    'humidity': parts[1],
                    'ph': parts[2],
                    'soil': parts[3],
                    'lux': parts[4]
                }
                socketio.emit('sensor_data', data)
        except Exception as e:
            print(f"Error reading serial: {e}")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    threading.Thread(target=read_from_arduino, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000)
