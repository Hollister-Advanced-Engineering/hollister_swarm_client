import wifi
import socketpool
import os
import time

WIFI_SSID = os.getenv("WIFI_SSID")
WIFI_PASSWORD = os.getenv("WIFI_SSID")

# --- Setup Wi-Fi ---
# Credentials should be in settings.toml as CIRCUITPY_WIFI_SSID and CIRCUITPY_WIFI_PASSWORD
print("Connecting to Wi-Fi...")
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
print(f"Connected! IP: {wifi.radio.ipv4_address}")

# Create a socket pool for networking
pool = socketpool.SocketPool(wifi.radio)

# --- Phase 1: UDP Discovery ---
udp_port = 50002
# Using a bytearray buffer as CircuitPython's recvfrom_into requires it
packet_buffer = bytearray(1024)

# Create and bind the UDP socket
udp_sock = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)
udp_sock.bind(('', udp_port)) # Listen on all interfaces at the discovery port
udp_sock.settimeout(None)     # Block until a packet is received

server_ip = None
server_tcp_port = None

print(f"Listening for discovery packets on UDP port {udp_port}...")

while not server_ip:
    # recvfrom_into returns (number of bytes received, (remote_ip, remote_port))
    size, addr = udp_sock.recvfrom_into(packet_buffer)
    # Decode only the bytes that were actually received
    msg = packet_buffer[:size].decode("utf-8")
    if msg.startswith("SERVER_IP_DISCOVERY"):
        server_ip = addr[0]
        # Assuming format "SERVER_IP_DISCOVERY:PORT"
        try:
            server_tcp_port = int(msg.split(":")[1])
            print(f"Found Server at {server_ip}:{server_tcp_port}")
        except (IndexError, ValueError):
            print("Received malformed discovery packet.")
            server_ip = None
udp_sock.close()

# --- Phase 2: TCP Connection ---
print(f"Connecting to TCP server at {server_ip}:{server_tcp_port}...")
tcp_client = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
tcp_client.connect((server_ip, server_tcp_port))
tcp_client.send(b"Hello from CircuitPython!")

# Keep connection alive or handle logic
while True:
    # Your logic here
    time.sleep(10)
