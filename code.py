"""
Hollister Swarm Client – CircuitPython (Annotated)

This program does three big things:

1. Connects the Raspberry Pi Pico W to Wi-Fi
2. Listens for a server broadcasting its location using UDP (discovery phase)
3. Connects to that server using TCP once discovered

Think of this like:
- UDP = "Anyone out there?"
- TCP = "Cool, now let's talk for real."
"""

# -------------------------
# Imports (libraries)
# -------------------------

import wifi          # Handles Wi-Fi radio on the Pico W
import socketpool    # Allows us to create network sockets
import time          # Used for delays (sleep)

# -------------------------
# Wi-Fi Credentials
# -------------------------
# These are hard-coded strings instead of environment variables
# so it's obvious what values are being used.

WIFI_SSID = "YOUR_WIFI_NAME"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

# -------------------------
# Step 1: Connect to Wi-Fi
# -------------------------

print("Connecting to Wi-Fi...")

# This tells the Pico W to connect to the access point
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)

# Once connected, the Pico is assigned an IP address by the router
print(f"Connected! IP address: {wifi.radio.ipv4_address}")

# -------------------------
# Step 2: Create a Socket Pool
# -------------------------
# A socket pool manages network connections.
# All UDP and TCP sockets will come from this pool.

pool = socketpool.SocketPool(wifi.radio)

# -------------------------
# Phase 1: UDP Discovery
# -------------------------
# The client does NOT know the server's IP address yet.
# Instead, it listens on a known UDP port for a broadcast message.

udp_port = 50002

# Buffer where incoming UDP packets will be stored
# 1024 bytes is plenty for a small discovery message
packet_buffer = bytearray(1024)

# Create a UDP socket
udp_sock = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)

# Bind the socket:
# '' means "listen on all network interfaces"
# udp_port is the port we expect discovery messages on
udp_sock.bind(('', udp_port))

# Block forever until a packet arrives
udp_sock.settimeout(None)

server_ip = None
server_tcp_port = None

print(f"Listening for discovery packets on UDP port {udp_port}...")

# Keep listening until we successfully discover the server
while not server_ip:

    # Receive data into the buffer
    # size = number of bytes received
    # addr = (remote_ip, remote_port)
    size, addr = udp_sock.recvfrom_into(packet_buffer)

    # Decode ONLY the received bytes (important!)
    msg = packet_buffer[:size].decode("utf-8")

    print(f"Received UDP message: {msg} from {addr}")

    # Expected format:
    # "SERVER_IP_DISCOVERY:PORT"
    if msg.startswith("SERVER_IP_DISCOVERY"):
        server_ip = addr[0]  # IP address of the sender

        try:
            # Extract TCP port number from the message
            server_tcp_port = int(msg.split(":")[1])
            print(f"Discovered server at {server_ip}:{server_tcp_port}")

        except (IndexError, ValueError):
            # If message format is wrong, reset and keep listening
            print("Malformed discovery packet received.")
            server_ip = None

# Once discovery is complete, close the UDP socket
udp_sock.close()

# -------------------------
# Phase 2: TCP Connection
# -------------------------
# Now that we know where the server is,
# we establish a reliable TCP connection.

print(f"Connecting to TCP server at {server_ip}:{server_tcp_port}...")

# Create a TCP socket
tcp_client = pool.socket(pool.AF_INET, pool.SOCK_STREAM)

# Connect to the server
tcp_client.connect((server_ip, server_tcp_port))

# Send a test message to confirm connection
tcp_client.send(b"Hello from CircuitPython!")

print("TCP connection established.")

# -------------------------
# Main Loop
# -------------------------
# This loop keeps the program alive.
# In the future, this is where:
# - sensor data would be sent
# - commands would be received
# - robot state would be updated

while True:
    print("Client alive and connected.")
    time.sleep(10)
