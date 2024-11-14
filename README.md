# Spherical Bot Application

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
   git clone https://github.com/kunalzambare972/sp-bot
   cd sp-bot

2. **Install the required Python libraries**:
   ```bash
   sudo ./requirements.sh

3. **Run the application on boot** (This is first time setup of raspberrypi only):</br>
   i. Create  a systemd service file:</br>
      ```
      sudo nano /etc/systemd/system/flask_app.service
      ```
   ii. Add the following configuration to the spbot.service file:</br>
      ```
      [Unit]
      Description=Spherical Robot Control 
      After=network.target

      [Service]
      ExecStart=/usr/bin/python3 /home/sp/sp-bot/app.py
      WorkingDirectory=/home/sp/sp-bot/
      Restart=always
      User=sp
      
      [Install]
      WantedBy=multi-user.target
      ```
      - Replace /home/sp/sp-bot/app.py with the actual path to your application.</br>
      - Replace /home/sp/sp-bot/ with the actual directory of your project.</br>
      - Replace the User= "sp" with your username. </br>

      
   iii. **Enable the service**:</br>
      ```
      sudo systemctl spbot.service
      ```
   
   iv. **Reload the system domain**:</br>
      ```
      sudo systemctl daemon-reload
      ```


   v. **To ensure pigpio and spbot flask serivceruns on boot for your Raspberry Pi Zero 2 W**:</br>
      - Create a systemd service file for pigpio:</br>
        ```
        sudo nano /etc/rc.local
        ```
      - Add the following text to the rc.local file between the if and fi lines of the rc.local script:</br>
        ```
        sudo pigpiod
        sudo systemctl start spbot.service
        ```
         
   vi. **Restart the Raspi Zero**:
      ```
      sudo reboot
      ```

   vi. **Check the status of spbot application service**:</br>
        ```
        sudo systemctl status spbot.service
        ```
## To access and interact with your the application:

1. **Ensure Both Devices Are on the Same Network**:</br>
   - Make sure your Android device and Raspberry Pi are connected to the same Wi-Fi network.</br>

2. **Find the Raspberry Pi’s IP Address**:</br>
   - You need the IP address of your Raspberry Pi to access the Flask application or else you can access it via hostname of the raspberry pi as well.</br>
   - To get the ip adress of the raspberry pi, download any network scanner application and scan the network for ip address, where you would get the ip of the raspberry pi.</br>
3. **Open a Web Browser on Your Android Device**</br>:
   - Launch a Web Browser: Open a web browser (such as Chrome, Firefox, or any other browser) on your Android device.</br>
   - Enter the IP Address and Port: Type the IP address of your Raspberry Pi followed by the port number where your Flask application is running. For example:</br>
     ```
      http://<your_raspberry_pi_ip>:5000

      or

      http://<your_raspberry_pi_hostname>:5000
      
      ```
      * Replace <your_raspberry_pi_ip> or <your_raspberry_pi_hostname> with the actual IP address or hostname of your Raspberry Pi respectively.</br>
      
3. **Access the Web Interface**:</br>
   - You should see the web interface of your Flask application.</br>
   
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
