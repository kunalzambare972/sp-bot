from flask import Flask, Response, render_template, request, redirect, url_for, session
import cv2
from picamera2 import Picamera2
import time
import pigpio
import numpy as np
import secrets
import hashlib

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generate a strong secret key

# Pre-initialized token
AUTHORIZED_TOKEN = 'sphericalbot_iitbombay'

# Initialize the camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (320, 240)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 15
picam2.configure("preview")
picam2.start()

# Initialize pigpio for servo and motor control
pi = pigpio.pi()
pi.set_mode(22, pigpio.OUTPUT)  # Front servo
pi.set_mode(23, pigpio.OUTPUT)  # Rear servo
pi.set_mode(13, pigpio.OUTPUT)  # PWMA
pi.set_mode(17, pigpio.OUTPUT)  # AIN2
pi.set_mode(18, pigpio.OUTPUT)  # AIN1
pi.set_mode(27, pigpio.OUTPUT)  # STBY

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'authenticated' in session and session['authenticated']:
        return render_template('control.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        token = request.form['token']
        if token == AUTHORIZED_TOKEN:
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            error = 'Invalid Token. Please try again.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.route('/video_feed')
def video_feed():
    if 'authenticated' in session and session['authenticated']:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return redirect(url_for('login'))

@app.route('/update_controls', methods=['POST'])
def update_controls():
    if 'authenticated' in session and session['authenticated']:
        motor_speed = int(request.form['motor_speed'])
        motor_direction = True if motor_speed > 0 else False
        motor_pwm = abs(motor_speed)
        servo_angle = int(request.form['servo_angle'])

        motor_control(motor_direction, motor_pwm)
        front_servo(servo_angle)
        rear_servo(servo_angle)
        return '', 200
    else:
        return redirect(url_for('login'))

def draw_arrow(frame):
    h, w, _ = frame.shape

    arrow_length = 150
    arrow_tip_length = 15

    start_pt = (w // 2, h - 20)
    end_pt = (w // 2, h - 20 - arrow_length)

    color = (0, 255, 0)
    thickness = 2

    cv2.arrowedLine(frame, start_pt, end_pt, color, thickness, tipLength=arrow_tip_length / arrow_length)

    return frame

def generate_frames():
    global fps_counter, latency
    prev_time = time.time()
    frame_count = 0

    while True:
        start_time = time.time()
        frame = picam2.capture_array()
        frame_count += 1
        end_time = time.time()
        latency = (end_time - start_time) * 1000

        if (end_time - prev_time) >= 1.0:
            fps_counter = frame_count / (end_time - prev_time)
            prev_time = end_time
            frame_count = 0

        overlay_frame = frame.copy()
        overlay_frame = draw_arrow(overlay_frame)
        cv2.putText(overlay_frame, f'FPS: {fps_counter:.2f}', (overlay_frame.shape[1] - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        cv2.putText(overlay_frame, f'Latency: {latency:.2f} ms', (overlay_frame.shape[1] - 150, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

        _, buffer = cv2.imencode('.jpg', overlay_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def front_servo(angle):
    pulse_width = map_value(-angle, -30, 30, 1300, 2000)
    pi.set_servo_pulsewidth(22, pulse_width)

def rear_servo(angle):
    pulse_width = map_value(angle, -30, 30, 1000, 1800)
    pi.set_servo_pulsewidth(23, pulse_width)

def motor_control(mot_dir, mot_pwm):
    if mot_dir:
        pi.write(27, 1)
        pi.write(18, 0)
        pi.write(17, 1)
        pi.set_PWM_dutycycle(13, mot_pwm)
    elif not mot_dir:
        pi.write(27, 1)
        pi.write(18, 1)
        pi.write(17, 0)
        pi.set_PWM_dutycycle(13, mot_pwm)
    else:
        pi.write(18, 0)
        pi.write(17, 0)
        pi.set_PWM_dutycycle(13, 0)
        pi.write(27, 0)

def map_value(value, axes_min, axes_max, actuate_min, actuate_max):
    axes_span = axes_max - axes_min
    actuate_span = actuate_max - actuate_min
    value_scaled = float(value - axes_min) / float(axes_span)
    return int(actuate_min + (value_scaled * actuate_span))

if __name__ == '__main__':
    fps_counter = 0
    latency = 0.0
    app.run(host='0.0.0.0', port=5000, threaded=True)
