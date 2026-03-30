# Step 2: Create Broadcast Listener
# listener.py
import socket
from config import PORT, BUFFER_SIZE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# สำหรับการรันหลาย Listener
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
sock.bind(("", PORT))  # Listen on all interfaces

print(f"[LISTENER] Listening for broadcast on port {PORT}")

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    print(f"[LISTENER] From {addr}: {data.decode()}")
