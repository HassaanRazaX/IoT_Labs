print("starting of neopixel flashing ")          # just checking printing output

from machine import Pin
from neopixel import NeoPixel
import time
import random


##################   Task 1   ##################

btn =Pin(4, Pin.IN, Pin.PULL_UP)    # same pin for physical esp32 s3 built in Boot buton

pin = Pin(48, Pin.OUT)              # set 48 for your physical esp32 s3

neo = NeoPixel(pin, 1)              # create NeoPixel driver  for 1 pixel

while True:
    while(btn.value()==1):          # flashing of neopixel stopped when button is in pressed status
        neo[0] = (255, 0, 0)            # set the first pixel to red
        print("red")
    
        neo.write()                     # write data to all pixels
        time.sleep(.2)
        neo[0] = (0, 255, 0)            # set the first pixel to green
        print("red")
    
        neo.write()                     # write data to all pixels
        time.sleep(.2)       
        neo[0] = (0, 0, 255)            # set the first pixel to blue
        print("blue")
    
        neo.write()                     # write data to all pixels
        time.sleep(.2) 
    

