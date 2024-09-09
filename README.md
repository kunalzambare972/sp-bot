# Spherical Bot Flask Based Control Application

This project allows you to control a Raspberry Pi Zero W-based robot using a Flask web application. The application streams live video from the Raspberry Pi's camera (using OpenCV and Picamera2) and provides motor and servo control through the web interface. It also supports IMU feedback via an Adafruit BNO055 sensor.

## Features
- Live camera streaming via Flask and OpenCV
- Motor speed control (N20 DC motors) using pigpio
- Servo control for directional movement
- Flask-based web interface for control
- IMU (BNO055) sensor integration for feedback

## Requirements

This project is built for Raspberry Pi Zero W, using the following main components:
- Raspberry Pi Zero W
- Camera module (e.g., OV5647 with 220 FOV fish-eye lens)
- Servo motors (for directional control)
- N20 DC motors (for movement)
- Adafruit BNO055 (IMU sensor)
- Flask for the web interface

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/Flask-RaspberryPi-Camera-Control.git
   cd Flask-RaspberryPi-Camera-Control
