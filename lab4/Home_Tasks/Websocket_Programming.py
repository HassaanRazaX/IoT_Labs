import network
import socket
import time
from machine import Pin, I2C
from neopixel import NeoPixel
import dht
import ssd1306  # Import OLED library

# WiFi Station Mode
ssid_st = "AAA"
password_st = "11111111"
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(ssid_st, password_st)

for _ in range(10):
    if sta.isconnected():
        break
    time.sleep(1)

if sta.isconnected():
    print("Connected to WiFi!")
    print("IP Address as station:", sta.ifconfig()[0])
else:
    print("Failed to connect")

# WiFi Access Point Mode
ssid_ap = "ESP32_AP"
password_ap = "12345678"
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid_ap, password=password_ap)
print("Access Point Active")
print("AP IP Address:", ap.ifconfig()[0])

# RGB LED Setup
pin = Pin(48, Pin.OUT)
neo = NeoPixel(pin, 1)

# DHT11 Sensor Setup
dht_pin = Pin(4)
dht_sensor = dht.DHT11(dht_pin)

def read_dht():
    try:
        dht_sensor.measure()
        return dht_sensor.temperature(), dht_sensor.humidity()
    except:
        return "Error", "Error"

# OLED Setup
i2c = I2C(scl=Pin(9), sda=Pin(8))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def update_oled(message):
    oled.fill(0)
    oled.text(message, 0, 0)
    oled.show()

# Web Page
def web_page(temp, hum):
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ESP32 Web Server</title>
        <style>
            body {{ font-family: Arial; text-align: center; background-color: #f8f9fa; }}
            button {{ padding: 10px; margin: 5px; font-size: 20px; }}
        </style>
    </head>
    <body>
        <h1>ESP32 Control Panel</h1>
        <h3>Temperature: {temp}&degC | Humidity: {hum}%</h3>
        <h2>RGB LED Control</h2>
        <form action="/" method="GET">
            <label>R:</label> <input type="number" name="R" min="0" max="255">
            <label>G:</label> <input type="number" name="G" min="0" max="255">
            <label>B:</label> <input type="number" name="B" min="0" max="255">
            <input type="submit" value="Set Color">
        </form>
        <h2>Display on OLED</h2>
        <form action="/"><input name="msg" type="text"><input type="submit" value="Send"></form>
    </body>
    </html>
    """
    return html

# Web Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print("Connection from:", addr)
    request = conn.recv(1024).decode()
    print("Request:", request)
    
    if "?R=" in request and "&G=" in request and "&B=" in request:
        try:
            r = int(request.split("R=")[1].split("&")[0])
            g = int(request.split("G=")[1].split("&")[0])
            b = int(request.split("B=")[1].split(" ")[0])
            neo[0] = (r, g, b)
            neo.write()
        except:
            pass
    elif "msg=" in request:
        msg = request.split("msg=")[1].split(" ")[0].replace("+", " ")
        update_oled(msg)
        
    temp, hum = read_dht()    
    response = web_page(temp, hum)
    conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n".encode())
    conn.send(response.encode())
    conn.close()

