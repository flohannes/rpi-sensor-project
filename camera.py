from picamera import PiCamera
from os import system
from time import sleep

camera = PiCamera()
camera.resolution = (1024, 768)

i=0
while True:
    i=i+1
    camera.capture('image{0:09d}.jpg'.format(i))
    sleep(10)
