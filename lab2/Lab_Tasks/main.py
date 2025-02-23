
# Task 1

# from machine import Pin
# from time import sleep

# btn =(0,Pin.IN,Pin.Pull_UP)

# while True:
#     sleep(.4)
#     print(btn.value())
    
# Task 2

# RGB light play
from machine import Pin
from neopixel import NeoPixel
import time

pin = Pin(48, Pin.OUT)   # set GPIO48  to output to drive NeoPixel
neo = NeoPixel(pin, 1)
while True:
    for i in range(0,255):# create NeoPixel driver on GPIO48 for 1 pixel
        for j in range(0,255):
            for k in range(0,255):
                neo[0] = (i, i-j, j) # set the first pixel to white
                time.sleep(.1)
                neo.write()              # write data to all pixels