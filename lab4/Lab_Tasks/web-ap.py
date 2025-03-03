import network
import socket
print("hhhhh")
# Setup Access Point
ssid = "ChanaChaat"
password = "12553"
#ap = network.WLAN(network.AP_IF)
#ap.active(True)
#ap.config(essid=ssid, password=password)

#print("Access Point Active, IP:", ap.ifconfig()[0])

# Start Web Server
def web_page():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IoT-AI6thSp25 ESP32 Web Server</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f4f4f4;
            color: #333;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #007bff;
        }
        .toggle-btn {
            display: inline-block;
            background: #007bff;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            cursor: pointer;
            transition: 0.3s;
        }
        .toggle-btn:hover {
            background: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>ESP32 Web Server</h1>
        <p>Welcome to ESP32 Web Server in AP Mode for the IoT class of AI6th in SP25!</p>
        <a href="#" class="toggle-btn" onclick="toggleDevice()">Toggle Device</a>
    </div>

    <script>
        function toggleDevice() {
            alert("Toggling device (this should send a request to the ESP32)");
            // Add code here to send an HTTP request to the ESP32 server
        }
    </script>
</body>
</html>
"""
    return html

# Setup Socket Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print("Connection from:", addr)
    request = conn.recv(1024)
    print("Request:", request)
    
    response = web_page()
    conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n")
    conn.send(response)
    conn.close()