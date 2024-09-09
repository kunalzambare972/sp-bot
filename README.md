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
   https://github.com/kunalzambare972/sp-bot
   cd sp-bot

2. **Install the required Python libraries**:
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt

3. **Run the application on boot**:</br>
   i. Create a systemd service file:</br>
      ```
      sudo nano /etc/systemd/system/flask_app.service
      ```
   ii. Add the following configuration to the flask_app.service file:</br>
      ```
      [Unit]
      Description=Spherical Robot Control using Flask 
      After=network.target

      [Service]
      ExecStart=/usr/bin/python3 /path/to/your/app.py
      WorkingDirectory=/path/to/your/project
      Restart=always
      User=pi
      Environment="PATH=/path/to/your/env/bin"
      
      [Install]
      WantedBy=multi-user.target
      ```
      - Replace /path/to/your/app.py with the actual path to your application.</br>
      - Replace /path/to/your/project with the actual directory of your project.</br>
      - Replace /path/to/your/env/bin with the actual path to your Python virtual environment.</br>
      - Replace the User= "pi" with your username. </br>
      
   iii. **Enable the service**:</br>
      ```
      sudo systemctl enable flask_app.service
      ```
   iv. **To ensure pigpio runs on boot for your Raspberry Pi Zero W**:</br>
      - Create a systemd service file for pigpio:</br>
        ```
        sudo nano /etc/systemd/system/pigpiod.service
        ```
      - Add the following configuration to the pigpiod.service file:</br>
        ```
        [Unit]
        Description=Pigpio daemon
        After=network.target

        [Service]
        ExecStart=/usr/bin/pigpiod
        Restart=always
        User=pi

        [Install]
        WantedBy=multi-user.target

        ```
        Replace the User= "pi" with your username.</br>
      - Enable the pigpiod service:</br>
         ```
         sudo systemctl enable pigpiod.service
         ```
         
   v. **Restart the Raspi Zero**:
      ```
      sudo reboot
      ```

   vi. **Check the status of pigpio and flask application service**:</br>
      - Check the status for Pigpio service:</br>
        ```
        sudo systemctl status pigpiod.service
        ```
      - Check the status of the Flask service:</br>
        ```
        sudo systemctl status flaskapp.service
        ```
   vii. **Test or Run the Flask application for Spherical Bot Control**:</br>
      ```
      http://<your_raspberry_pi_ip>:5000

      or

      http://<your_raspberry_pi_hostname>:5000
      
      ```
      Replace <your_raspberry_pi_ip> or <your_raspberry_pi_hostname> with the actual IP address or hostname of your Raspberry Pi respectively.</br>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
