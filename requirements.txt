#!/bin/bash

# Update package list and install Python pip if not already installed
echo "Updating package list..."
sudo apt update

echo "Installing pip for Python 3..."
sudo apt install -y python3-pip

# Install each required Python package one by one
echo "Installing Flask..."
pip3 install Flask

echo "Installing pigpio..."
pip3 install pigpio

echo "Installing pybind11..."
pip3 install pybind11

echo "Installing numpy..."
pip3 install numpy

echo "Installing OpenCV..."
pip3 install opencv-python

echo "Installing Adafruit CircuitPython BNO055..."
pip3 install adafruit-circuitpython-bno055

echo "Installing Adafruit CircuitPython BusDevice..."
pip3 install adafruit-circuitpython-busdevice

echo "Installing Adafruit CircuitPython Register..."
pip3 install adafruit-circuitpython-register

echo "Installing Adafruit Blinka..."
pip3 install adafruit-blinka

echo "All packages installed successfully."
