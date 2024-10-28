from flask import Flask, render_template, Response, request, jsonify
import pigpio
import os
import subprocess

# Initialize Flask application
app = Flask(__name__)

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

# HLS configuration
HLS_DIR = "hls"
os.makedirs(HLS_DIR, exist_ok=True)

# Function to start HLS streaming
def start_hls_stream():
    cmd = [
        'ffmpeg',
        '-f', 'v4l2',  # Use video4linux2 input
        '-i', '/dev/video0',  # Adjust this if your camera is on a different device
        '-preset', 'veryfast',
        '-vf', 'scale=640:480',  # Scale to 640x480
        '-hls_time', '2',  # Duration of each segment
        '-hls_list_size', '0',  # Unlimited number of playlist entries
        '-hls_wrap', '0',  # Don't wrap around
        '-start_number', '0',
        os.path.join(HLS_DIR, 'output.m3u8')  # Output playlist file
    ]
    
    # Run ffmpeg as a subprocess
    subprocess.Popen(cmd)

# Start HLS stream
start_hls_stream()

# Function to control motors
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

# Function to sync servos
def sync_servos(angle):
    pulse_width_1 = map_value(-angle, -90, 90, 1000, 2000)
    pulse_width_2 = map_value(angle, -90, 90, 1000, 2000)
    pi.set_servo_pulsewidth(22, pulse_width_1)
    pi.set_servo_pulsewidth(23, pulse_width_2)

# Route for video feed
@app.route('/video_feed')
def video_feed():
    return Response(open(os.path.join(HLS_DIR, 'output.m3u8')), mimetype='application/vnd.apple.mpegurl')

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
