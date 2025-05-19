from flask import Flask, render_template, Response, send_file
from flask_socketio import SocketIO
from flask_cors import CORS
import serial
import threading
import cv2
import io
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Adjust the serial port as necessary (e.g., /dev/ttyUSB0, /dev/ttyACM0)
ser = serial.Serial('/dev/ttyUSB0', 9600)

# Global camera object
camera = None

def get_camera():
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return camera

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

                # Emit to frontend
                socketio.emit('sensor_data', data)

                # Print to terminal
                print("[Sensor Readings]")
                print(f"  Temperature: {data['temperature']} °C")
                print(f"  Humidity   : {data['humidity']} %")
                print(f"  pH Value   : {data['ph']}")
                print(f"  Soil Moist.: {data['soil']}")
                print(f"  Light Lux  : {data['lux']}")
                print("--------------------------\n")
        except Exception as e:
            print(f"[ERROR] Serial read failed: {e}")

def generate_camera():
    camera = get_camera()
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Resize frame for better mobile performance
            frame = cv2.resize(frame, (640, 480))
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_camera(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture_image')
def capture_image():
    camera = get_camera()
    success, frame = camera.read()
    if not success:
        return "Failed to capture image", 500
    
    # Resize frame for better quality
    frame = cv2.resize(frame, (640, 480))
    
    # Convert to JPEG
    ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
    if not ret:
        return "Failed to encode image", 500
    
    # Create in-memory file
    img_io = io.BytesIO(buffer)
    img_io.seek(0)
    
    return send_file(
        img_io,
        mimetype='image/jpeg',
        as_attachment=True,
        download_name=f'plant_capture_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.jpg'
    )

if __name__ == '__main__':
    threading.Thread(target=read_from_arduino, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
