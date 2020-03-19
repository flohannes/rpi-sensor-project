import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from os import system

GPIO.setmode(GPIO.BCM)
PIR_PIN = 23
GPIO.setup(PIR_PIN, GPIO.IN)
camera = PiCamera()
camera.resolution = (1024, 768)

i=0
try:
    print "PIR Module Test (CTRL+C to exit)"
    time.sleep(2)
    print "Ready"
    while True:
        if GPIO.input(PIR_PIN):
            i=i+1
            print "Motion Detected!"
            camera.capture('alarm-image{0:09d}.jpg'.format(i))
            time.sleep(10) 
        time.sleep(1)
except KeyboardInterrupt:
    print " Quit"
    GPIO.cleanup()


