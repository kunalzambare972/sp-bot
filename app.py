from flask import Flask, render_template, Response, request, jsonify
import pigpio
import busio
import board
import time
from picamera2 import Picamera2
import cv2

# Initialize Flask application
app = Flask(__name__)

# Initialize camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (320, 240)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 15  # Set FPS
picam2.configure("preview")
picam2.start()

# Initialize pigpio for servo and motor control
pi = pigpio.pi()
pi.set_mode(22, pigpio.OUTPUT)  # Servo 1
pi.set_mode(23, pigpio.OUTPUT)  # Servo 2
pi.set_mode(13, pigpio.OUTPUT)  # Motor PWM
pi.set_mode(17, pigpio.OUTPUT)  # Motor AIN2
pi.set_mode(18, pigpio.OUTPUT)  # Motor AIN1
pi.set_mode(27, pigpio.OUTPUT)  # Motor STBY

# IMU Setup (commented out)
# i2c = busio.I2C(board.SCL, board.SDA)
# sensor = adafruit_bno055.BNO055_I2C(i2c)

# Global variables
fps_counter = 0
latency = 0.0
motor_speed = 50  # Default speed
servo_angle = 0   # Default servo angle

# Mapping function for scaling values
def map_value(value, axes_min, axes_max, actuate_min, actuate_max):
    axes_span = axes_max - axes_min
    actuate_span = actuate_max - actuate_min
    value_scaled = float(value - axes_min) / float(axes_span)
    return int(actuate_min + (value_scaled * actuate_span))

# Motor control function
def control_motor(direction, speed):
    if direction:
        pi.write(27, 1)  # Disable standby (active low)
        pi.write(18, 0)
        pi.write(17, 1)
        pi.set_PWM_dutycycle(13, speed)
    else:
        pi.write(27, 1)  # Disable standby (active low)
        pi.write(18, 1)
        pi.write(17, 0)
        pi.set_PWM_dutycycle(13, speed)

# Servo control function
def sync_servos(angle):
    pulse_width_1 = map_value(-angle, -30, 30, 1300, 2000)
    pulse_width_2 = map_value(angle, -30, 30, 1000, 1800)
    pi.set_servo_pulsewidth(22, pulse_width_1)
    pi.set_servo_pulsewidth(23, pulse_width_2)

# Video feed generation
def generate_frames():
    global fps_counter, latency
    prev_time = time.time()
    frame_count = 0

    while True:
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

        # Draw FPS and latency on frame
        cv2.putText(frame, f'FPS: {fps_counter:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        cv2.putText(frame, f'Latency: {latency:.2f} ms', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route for video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Home route serving the control page
@app.route('/')
def index():
    return render_template('index.html')  # Ensure your HTML file is named index.html

# Route to handle control commands
@app.route('/control', methods=['POST'])
def control():
    global motor_speed, servo_angle
    data = request.json
    if 'motor_speed' in data:
        motor_speed = int(data['motor_speed'])
        direction = motor_speed >= 50  # Forward if above 50, backward otherwise
        speed = abs(motor_speed - 50) * 2  # Scale speed (0-100)
        control_motor(direction, speed)

    if 'servo_angle' in data:
        servo_angle = int(data['servo_angle']) - 50  # Center at 0
        sync_servos(servo_angle)

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
