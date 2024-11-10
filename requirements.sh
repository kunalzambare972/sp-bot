#!/bin/bash

# Update package list
sudo apt update

# Install Python 3 and pip3 if not already installed
sudo apt install -y python3 python3-pip

# Install pigpio for GPIO control
sudo apt install -y pigpio

# Install Python development headers and dependencies
sudo apt install -y python3-dev libjpeg-dev libtiff-dev libatlas-base-dev

# Install numpy and Pillow (dependencies for image processing)
pip3 install numpy --break-system-packages
pip3 install Pillow --break-system-packages

# Install OpenCV
sudo apt install -y python3-opencv

# Install Flask and related Python libraries
pip3 install Flask --break-system-packages
pip3 install Jinja2 --break-system-packages
pip3 install Werkzeug --break-system-packages
pip3 install itsdangerous --break-system-packages
pip3 install click --break-system-packages
pip3 install flask-json --break-system-packages

# Install Adafruit libraries (available only via pip)
pip3 install adafruit-circuitpython-bno055 --break-system-packages
pip3 install adafruit-circuitpython-busdevice --break-system-packages
pip3 install adafruit-circuitpython-register --break-system-packages
pip3 install Adafruit-Blinka --break-system-packages

