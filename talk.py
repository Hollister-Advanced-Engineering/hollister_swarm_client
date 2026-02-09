import wifi
import socketpool
import os
import time
import board
import busio
import usb_cdc # 🔹 ADDED
import adafruit_ssd1306

WIFI_SSID = "waran"
WIFI_PASSWORD = "DeepSpace6884"

oled_width = 128
oled_height = 64

i2c = busio.I2C(scl=board.GP5, sda=board.GP4)
oled = adafruit_ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# --- USB Console ---
console = usb_cdc.console # 🔹 ADDED
console.timeout = 0 # 🔹 NON-BLOCKING READ

# --- Setup Wi-Fi ---
print("Connecting to Wi-Fi...")
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
print("Connected! IP:", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)

# --- Phase 1: UDP Discovery ---
udp_port = 50002
packet_buffer = bytearray(1024)

udp_sock = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)
udp_sock.bind(("", udp_port))
udp_sock.settimeout(None)

server_ip = None
server_tcp_port = None

print("Listening for discovery packets...")

while not server_ip:
    size, addr = udp_sock.recvfrom_into(packet_buffer)
    msg = packet_buffer[:size].decode("utf-8").strip()

    if msg.startswith("SERVER_IP_DISCOVERY"):
        server_ip = addr[0]
        try:
            server_tcp_port = int(msg.split(":")[1])
            print("Found server:", server_ip, server_tcp_port)
        except:
            server_ip = None

udp_sock.close()

# --- Phase 2: TCP Connection ---
print("Connecting to TCP server...")
tcp_client = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
tcp_client.connect((server_ip, server_tcp_port))
tcp_client.send(b"Phoenix team connected!!\n")


# --- Main Loop ---
buffer = b"" # 🔹 INPUT BUFFER

while True:
    try:
        user_input = input() # ← THIS is the key fix
        if user_input:
            print("Sending:", user_input)
            tcp_client.send((user_input + "\n").encode("utf-8"))

            oled.fill(0)
            oled.text("Sent:", 0, 0, 1)
            oled.text(user_input[:16], 0, 12, 1)
            oled.show()

    except Exception as e:
        print("Error:", e)

    time.sleep(0.01)
