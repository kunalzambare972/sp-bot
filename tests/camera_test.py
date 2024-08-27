from flask import Flask, Response, render_template_string
import cv2
from picamera2 import Picamera2
import time
import numpy as np

app = Flask(__name__)

# Initialize the camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (320, 240)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 15  # Set to desired FPS (e.g., 15)
picam2.configure("preview")
picam2.start()

# HTML template to display the video feed
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Live Stream</title>
    <style>
        body { font-family: Arial, sans-serif; zoom: 200%; } /* Zoom the page */
        #video { width: 100%; }
    </style>
</head>
<body>
    <h1>Live Stream</h1>
    <img id="video" width="640" height="480" src="{{ url_for('video_feed') }}" />
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def draw_arrow(frame):
    h, w, _ = frame.shape

    # Define arrow parameters
    arrow_length = 150  # Length of the arrow (adjust as needed)
    arrow_tip_length = 15  # Length of the arrow tip (adjust as needed)
    
    # Calculate start and end points to center the arrow horizontally
    start_pt = (w // 2, h - 20)  # Start point of the arrow (bottom center)
    end_pt = (w // 2, h - 20 - arrow_length)  # End point of the arrow (pointing upwards)

    color = (0, 255, 0)  # Green color in BGR
    thickness = 2        # Thickness of the arrow

    # Draw the vertical arrowed line
    cv2.arrowedLine(frame, start_pt, end_pt, color, thickness, tipLength=arrow_tip_length / arrow_length)

    return frame

def generate_frames():
    global fps_counter, latency
    prev_time = time.time()
    frame_count = 0

    while True:
        try:
            start_time = time.time()
            frame = picam2.capture_array()
            frame_count += 1
            end_time = time.time()
            latency = (end_time - start_time) * 1000  # Convert to milliseconds

            # Calculate FPS
            if (end_time - prev_time) >= 1.0:
                fps_counter = frame_count / (end_time - prev_time)
                prev_time = end_time
                frame_count = 0

            # Draw the arrow and overlay FPS and latency
            overlay_frame = frame.copy()
            overlay_frame = draw_arrow(overlay_frame)
            cv2.putText(overlay_frame, f'FPS: {fps_counter:.2f}', (overlay_frame.shape[1] - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
            cv2.putText(overlay_frame, f'Latency: {latency:.2f} ms', (overlay_frame.shape[1] - 150, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

            _, buffer = cv2.imencode('.jpg', overlay_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print(f"Error generating frames: {e}")
            break

if __name__ == '__main__':
    # Initialize global variables
    fps_counter = 0
    latency = 0.0
    # Run the Flask app on localhost with a fixed port
    app.run(host='0.0.0.0', port=5000, threaded=True)
