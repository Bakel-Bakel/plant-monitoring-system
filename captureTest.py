import cv2
import os
import time
from datetime import datetime

# Folder to save images
DATASET_FOLDER = 'plantDataset'
os.makedirs(DATASET_FOLDER, exist_ok=True)

# Open the USB camera (0 = default camera)
camera = cv2.VideoCapture(0)

# Optional: set camera resolution
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("[INFO] Starting image capture every 30 seconds...")

try:
    while True:
        # Read a frame from the camera
        success, frame = camera.read()
        if success:
            # Generate timestamped filename
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = os.path.join(DATASET_FOLDER, f'{timestamp}.jpg')

            # Save the frame
            cv2.imwrite(filename, frame)
            print(f"[INFO] Saved image: {filename}")
        else:
            print("[WARNING] Failed to capture image from camera")

        # Wait 30 seconds
        time.sleep(30)

except KeyboardInterrupt:
    print("\n[INFO] Image capture stopped by user.")

finally:
    # Release the camera
    camera.release()

