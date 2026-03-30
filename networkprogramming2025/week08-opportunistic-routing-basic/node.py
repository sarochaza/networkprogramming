#node.py
import socket
import threading
import time
import sys
from config import HOST, BUFFER_SIZE, FORWARD_THRESHOLD, UPDATE_INTERVAL
from delivery_table import DeliveryTable

# รับ port จาก command line
BASE_PORT = int(sys.argv[1])

# peers = port ที่เหลือ
PEER_PORTS = [int(p) for p in sys.argv[2:]]

delivery_table = DeliveryTable()
message_queue = []

def send_message(peer_port, message):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((HOST, peer_port))
        s.sendall(message.encode())
        s.close()
        print(f"[NODE {BASE_PORT}] Sent: {message} to {peer_port}")
        return True
    except (ConnectionRefusedError, socket.timeout):
        return False


def forward_loop():
    while True:
        candidates = delivery_table.get_best_candidates(FORWARD_THRESHOLD)

        for msg in message_queue[:]:
            for peer in candidates:
                if send_message(peer, msg):
                    message_queue.remove(msg)
                    break

        time.sleep(UPDATE_INTERVAL)


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, BASE_PORT))
    server.listen()

    print(f"[NODE {BASE_PORT}] Listening...")

    while True:
        conn, addr = server.accept()
        data = conn.recv(BUFFER_SIZE).decode()
        print(f"[NODE {BASE_PORT}] Received: {data}")
        message_queue.append(data)
        conn.close()


if __name__ == "__main__":
    # เริ่ม server และ forwarding thread
    threading.Thread(target=start_server, daemon=True).start()
    threading.Thread(target=forward_loop, daemon=True).start()

    # ตั้งค่า probability ให้ peers
    for peer in PEER_PORTS:
        delivery_table.update_probability(peer, 0.6)

    # ส่งข้อความเริ่มต้น
    for peer in PEER_PORTS:
        msg = f"Hello from node {BASE_PORT}"
        if not send_message(peer, msg):
            print(f"[NODE {BASE_PORT}] Store message for {peer}")
            message_queue.append(msg)

    while True:
        time.sleep(1)

        