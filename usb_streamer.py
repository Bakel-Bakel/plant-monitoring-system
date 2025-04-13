from flask import Flask, Response
import cv2

app = Flask(__name__)

# Open the USB webcam (usually 0, or try 1 if it doesn't work)
camera = cv2.VideoCapture(0)

# Optionally, set the resolution (adjust as needed)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
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
    app.run(host='0.0.0.0', port=5000)

