print("Hello, ESP32-S3!")

import network
import socket
import time
from machine import Pin,I2C
from neopixel import NeoPixel
import dht
import ssd1306





ssid_st = "300C"
password_st = "Hashim000"

print("Connecting to WiFi", end="")
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(ssid_st,password_st)

# Wait for connection
for _ in range(10):
    if sta.isconnected():
        break
    time.sleep(1)
    
    
if sta.isconnected():
    print("Connected to WiFi!")
    print("IP Address as station:", sta.ifconfig()[0])
else:
    print("Failed to connect")
    




ssid_ap = "ESP32_AP"
password_ap = "12345678"  # Minimum 8 characters
auth_mode = network.AUTH_WPA2_PSK  # Secure mode (recommended)

# Create an Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)  # Activate AP mode
ap.config(essid=ssid_ap, password=password_ap, authmode=auth_mode)  # Set SSID and password

print("Access Point Active")
print("AP IP Address:", ap.ifconfig()[0])



#####################OLED########################
# Initialize OLED display
i2c = I2C(scl=Pin(9), sda=Pin(8))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

oled.fill(0)
oled.text("hello", 0, 0)
oled.show()

def update_oled(message):
    oled.fill(0)
    oled.text(message, 0, 0)
    oled.show()

#####################OLED########################
dht_pin=4

dht_sensor=dht.DHT11(Pin(dht_pin))
                     

#DHT meausure

def dht():
    dht_sensor.measure()
    time.sleep(0.2)
    temp = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    return temp,humidity

pin = Pin(48, Pin.OUT)   # set GPIO48  to output to drive NeoPixel
neo = NeoPixel(pin, 1)   # create NeoPixel driver on GPIO48 for 1 pixelStart

#Web Server
def web_page():
    temp,humidity=dht()
    html = f"""<!DOCTYPE html>
    <html>
    <head><title>ESP32 RGB LED Control</title></head>
    <body>
    <h1>ESP32 RGB LED Control</h1>
    <p><a href="/?RGB=red"><button>Turn RGB RED</button></a></p>
    <p><a href="/?RGB=green"><button>Turn RGB GREEN</button></a></p>
    <p><a href="/?RGB=blue"><button>Turn RGB BLUE</button></a></p>
    <br>
    <h1>Temperature and Humidity</h1>
    <h2>Temp: {temp}°C</h2>
    <h2>Humidity: {humidity}%</h2>
    <br>
    <br>
    <h2>Display on OLED</h2>
    <form action="/"><input name="msg" type="text"><input type="submit" value="Send"></form>

    </body>
    </html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print("Connection from:", addr)
    request = conn.recv(1024).decode()
    print("Request:", request)
    
    if "/?RGB=red" in request:
        neo[0] = (255, 0, 0) # set the first pixel to red
        neo.write()              # write data to all pixels
    elif "/?RGB=green" in request:
        neo[0] = (0, 255, 0) # set the first pixel to green
        neo.write()              # write data to all pixels
    elif "/?RGB=blue" in request:
        neo[0] = (0, 0, 255) # set the first pixel to blue
        neo.write()              # write data to all pixels
        
    elif "msg=" in request:
        msg = request.split("msg=")[1].split(" ")[0].replace("+", " ")
        print(msg)
        update_oled(msg)
        
    response = web_page()
    conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n")
    conn.send(response)
    conn.close()




