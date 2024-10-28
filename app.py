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
try:
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (640, 480)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.controls.FrameRate = 10  # Set FPS
    picam2.configure("preview")
    picam2.start()
except Exception as e:
    print(f"Error initializing camera: {e}")

# Initialize pigpio for servo and motor control
pi = pigpio.pi()
pi.set_mode(22, pigpio.OUTPUT)  # Servo 1
pi.set_mode(23, pigpio.OUTPUT)  # Servo 2
pi.set_mode(13, pigpio.OUTPUT)  # Motor PWM
pi.set_mode(17, pigpio.OUTPUT)  # Motor AIN2
pi.set_mode(18, pigpio.OUTPUT)  # Motor AIN1
pi.set_mode(27, pigpio.OUTPUT)  # Motor STBY

# Global variables
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
    pulse_width_1 = map_value(-angle, -90, 90, 1000, 2000)
    pulse_width_2 = map_value(angle, -90, 90, 1000, 2000)
    pi.set_servo_pulsewidth(22, pulse_width_1)
    pi.set_servo_pulsewidth(23, pulse_width_2)

# Video feed generation
def generate_frames():
    while True:
        try:
            frame = picam2.capture_array()
            # Encode frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print(f"Error capturing frame: {e}")
            break

# Route for video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Home route serving the control page
@app.route('/')
def index():
    return render_template('index.html')  # Ensure HTML file is named index.html

# Route to handle control commands
@app.route('/control', methods=['POST'])
def control():
    global motor_speed, servo_angle
    data = request.json
    if 'motor_speed' in data:
        motor_speed = int(data['motor_speed'])
        direction = motor_speed >= 50  # Forward if above 50, backward otherwise
        
        # Calculate the speed and restrict to a max of 165 (65% of 255)
        speed = abs(motor_speed - 50) * 2  # Scale speed (0-100)
        max_speed = 165  # 65% of the max duty cycle for the motor
        
        # Ensure speed does not exceed max_speed
        speed = min(speed, max_speed)

        control_motor(direction, speed)

    if 'servo_angle' in data:
        servo_angle = int(data['servo_angle']) - 50  # Center at 0
        sync_servos(servo_angle)

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)