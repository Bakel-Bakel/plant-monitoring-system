from flask import Flask, Response
import cv2
import os
import time
import threading
from datetime import datetime

app = Flask(__name__)

# Create dataset folder if it doesn't exist
DATASET_FOLDER = 'plantDataset'
os.makedirs(DATASET_FOLDER, exist_ok=True)

# Open the USB webcam (0 or 1 depending on your camera index)
camera = cv2.VideoCapture(0)

# Optionally, set the resolution
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Shared frame for both streaming and saving
current_frame = None

def capture_images_periodically():
    global current_frame
    while True:
        if current_frame is not None:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = os.path.join(DATASET_FOLDER, f'{timestamp}.jpg')
            cv2.imwrite(filename, current_frame)
            print(f"[INFO] Saved image: {filename}")
        time.sleep(30)  # Capture every 30 seconds

def generate_frames():
    global current_frame
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            current_frame = frame.copy()
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def home():
    return '<h1>USB Webcam Stream</h1><img src="/video">'

if __name__ == '__main__':
    # Start the background image capture thread
    threading.Thread(target=capture_images_periodically, daemon=True).start()

    app.run(host='0.0.0.0', port=5000)
