#!/bin/bash

# Update package list and install Python pip if not already installed
echo "Updating package list..."
sudo apt update

echo "Installing pip for Python 3..."
sudo apt install -y python3-pip

# Install each required Python package one by one
echo "Installing Flask..."
pip3 install Flask --break-system-packages

echo "Installing pigpio..."
pip3 install pigpio --break-system-packages

echo "Installing pybind11..."
pip3 install pybind11 --break-system-packages

echo "Installing numpy..."
pip3 install numpy --break-system-packages

echo "Installing OpenCV..."
pip3 install opencv-python --break-system-packages

echo "Installing Adafruit CircuitPython BNO055..."
pip3 install adafruit-circuitpython-bno055 --break-system-packages

echo "Installing Adafruit CircuitPython BusDevice..."
pip3 install adafruit-circuitpython-busdevice --break-system-packages

echo "Installing Adafruit CircuitPython Register..."
pip3 install adafruit-circuitpython-register --break-system-packages

echo "Installing Adafruit Blinka..."
pip3 install adafruit-blinka --break-system-packages

echo "All packages installed successfully."
