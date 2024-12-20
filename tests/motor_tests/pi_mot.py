#!/usr/bin/env python
'''
Pigpio is better than Rpi.GPIO. Fast and no jitter in pwm signals
MOTOR CONTROL using RPI and N20 dc motor and motor driver Motor Driver - Dual TB6612FNG (1A)

PINOUT for implementation

7  - GPIO 13  -> PWM  Hardware PWM
11 - GPIO 17 -> AIN2
12 - GPIO 18 -> AIN1
13 - GPIO 27 -> STBY (Standby) Active low

Project - Small spherical bot
Vaibhav Kadam
27 Aug 2019
'''

import time
import pigpio

pi = pigpio.pi()

'''
    pi.setmode(GPIO_ pin number, IN/OUT)

 '''

pi.set_mode(13,pigpio.OUTPUT)  #PWMA 13         7
pi.set_mode(17,pigpio.OUTPUT)  #AIN2 17       11
pi.set_mode(18,pigpio.OUTPUT)  #AIN1 18        12
pi.set_mode(27,pigpio.OUTPUT)  #STBY 27        13


#pi.write(27,0) #   

counter = 0
while(counter<=1):
    counter+=1
    
    #Clockwise direction 
    # print "Clockwise direction"
    pi.write(27,1) #disable standby active low
    pi.write(18,1)
    pi.write(17,0)
    pi.set_PWM_dutycycle(13,125)
    #pi.hardware_PWM(13, 800, 400000) # 800Hz 75% dutycycle
    time.sleep(2)
   

    
    #Anti Clockwise direction
    #print "Anti Clockwise direction"
    #pi.write(27,1)
    pi.write(18,0)
    pi.write(17,1)
    pi.set_PWM_dutycycle(13, 50)
    #pi.hardware_PWM(13, 800, 400000) # 800Hz 75% dutycycle
    time.sleep(2)
    
    

pi.write(18,0)
pi.write(17,0)
pi.set_PWM_dutycycle(13, 0)
pi.write(27,0)
pi.stop()


