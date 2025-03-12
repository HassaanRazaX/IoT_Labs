import network
import time
import socket
from machine import Pin, I2C
from neopixel import NeoPixel
import dht
import json
from ssd1306 import SSD1306_I2C  # OLED display library
import usocket as socket
import uwebsockets as websockets

# DHT Sensor setup
dht_pin = 4
dht_sensor = dht.DHT11(Pin(dht_pin))

# NeoPixel setup
pin = Pin(48, Pin.OUT)
neo = NeoPixel(pin, 1)

# OLED Display setup
i2c = I2C(0, scl=Pin(9), sda=Pin(8))  # Use GPIO9 for SCL and GPIO8 for SDA
oled = SSD1306_I2C(128, 64, i2c)  # Change to 128x32 if using a smaller display
print("OLED initialized")

# WiFi credentials
ssid_st = "NTU FSD"
password_st = ""

# Connect to WiFi
print("Connecting to WiFi", end="")
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(ssid_st, password_st)

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

# Access Point setup
ssid_ap = "ESP_1354"
password_ap = "12345678"
auth_mode = network.AUTH_WPA2_PSK

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid_ap, password=password_ap, authmode=auth_mode)

print("Access Point Active")
print("AP IP Address:", ap.ifconfig()[0])

# Function to read DHT sensor with error handling
def read_dht_sensor():
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        return temp, humidity
    except Exception as e:
        print("Failed to read DHT sensor:", e)
        return None, None

def update_oled(message):
    oled.fill(0)
    oled.text(message, 0, 0)
    oled.show()

def web_page():
    html = """<!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>ESP32 Weather Station</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #1e1e2f;
                color: #ffffff;
                margin: 0;
                padding: 20px;
                text-align: center;
            }
            h1 {
                color: #ff6f61;
                font-size: 2.5em;
                margin-bottom: 20px;
            }
            h2 {
                color: #a8e6cf;
                font-size: 1.8em;
                margin: 10px 0;
            }
            .sensor-data {
                background-color: #2e2e4a;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
                display: inline-block;
                margin-top: 20px;
            }
            .emoji {
                font-size: 1.5em;
            }
            .alert {
                font-size: 1.2em;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }
            .alert.high-temp {
                background-color: #ff6f61;
            }
            .alert.high-humidity {
                background-color: #008CBA;
            }
        </style>
        <script>
            var ws = new WebSocket('ws://' + window.location.host + '/ws');
            ws.onmessage = function(event) {
                var data = JSON.parse(event.data);
                document.getElementById('temp').innerText = data.temp + " °C 🌡️";
                document.getElementById('humidity').innerText = data.humidity + " % 💧";
                
                var alertDiv = document.getElementById('alert');
                alertDiv.innerHTML = '';
                if (data.temp > 30) {
                    alertDiv.innerHTML = '<div class="alert high-temp">🌡️ High Temperature! 🔥</div>';
                    ws.send('RGB:255,0,0');
                } else if (data.humidity > 70) {
                    alertDiv.innerHTML = '<div class="alert high-humidity">💧 High Humidity! 💦</div>';
                    ws.send('RGB:0,0,255');
                } else {
                    ws.send('RGB:0,255,0');
                }
            };
        </script>
    </head>
    <body>
        <h1>ESP32 Weather Station</h1>
        <div class="sensor-data">
            <h1>🌡️ TEMPERATURE AND HUMIDITY 💧</h1>
            <h2>Temp: <span id="temp">N/A</span></h2>
            <h2>Humidity: <span id="humidity">N/A</span></h2>
            <div id="alert"></div>
        </div>
    </body>
    </html>"""
    return html

# Start web server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 80))
s.listen(5)

# WebSocket handler
def handle_websocket(ws):
    while True:
        temp, humidity = read_dht_sensor()
        if temp is None or humidity is None:
            temp = "N/A"
            humidity = "N/A"
        sensor_data = {"temp": temp, "humidity": humidity}
        ws.send(json.dumps(sensor_data))
        time.sleep(2)

# Main loop
while True:
    conn, addr = s.accept()
    print("Connection from:", addr)
    request = conn.recv(1024).decode()
    print("Request:", request)
    
    if request.startswith("GET /ws"):
        print("WebSocket request")
        ws = websockets.server(conn)
        handle_websocket(ws)
    elif request.startswith("GET / "):
        response = web_page()
        conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n")
        conn.send(response)
    elif request.startswith("POST /RGB"):
        data = request.split("\r\n\r\n")[1]
        r, g, b = map(int, data.split(','))
        neo[0] = (r, g, b)
        neo.write()
        conn.send("HTTP/1.1 200 OK\n\n")
    
    conn.close()