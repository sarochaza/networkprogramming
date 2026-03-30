# node.py
import socket
import threading
import random
from config import HOST, BASE_PORT, BUFFER_SIZE, NEIGHBORS, FORWARD_PROBABILITY, TTL

neighbor_table = set(NEIGHBORS)

# ============================================================
# 1. จัดการข้อความที่ได้รับ (Handle Incoming)
# ============================================================
def handle_incoming(conn, addr):
    try:
        data = conn.recv(BUFFER_SIZE).decode()
        if not data:
            return
        
        # แยกข้อมูลออกเป็น 3 ส่วน (พอร์ตต้นทาง, TTL, ข้อความ)
        # ใช้ .split('|', 2) เพื่อป้องกัน error ถ้าในข้อความบังเอิญมีตัว | พิมพ์ติดมาด้วย
        parts = data.split('|', 2)
        if len(parts) == 3:
            sender_port_str, ttl_str, msg = parts
            sender_port = int(sender_port_str) # พอร์ตจริงๆ ของคนที่ส่งมา
            ttl = int(ttl_str)
        else:
            print(f"[NODE {BASE_PORT}] Received malformed data")
            return

        print(f"[NODE {BASE_PORT}] Received from Node {sender_port}: '{msg}' (TTL={ttl})")
        
        # สุ่มส่งต่อ (Forward) ถ้า TTL ยังเหลือ
        if ttl > 0 and random.random() < FORWARD_PROBABILITY:
            print(f"  -> [FORWARDING] Decided to forward '{msg}' (New TTL={ttl - 1})")
            # เวลาส่งต่อ เราจะระบุไม่ให้ส่งกลับไปหา sender_port ตัวจริง
            forward_message(msg, ttl - 1, exclude=sender_port)

    except Exception as e:
        print(f"[NODE {BASE_PORT}] Error: {e}")
    finally:
        conn.close()

# ============================================================
# 2. เปิด Server รอรับการเชื่อมต่อ (Start Server)
# ============================================================
def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # ป้องกันพอร์ตค้าง
    server.bind((HOST, port))
    server.listen(10)
    print(f"[NODE {port}] Listening for neighbors...")
    
    while True:
        conn, addr = server.accept()
        # โยนให้ Thread จัดการ เพื่อให้รับสายคนอื่นต่อได้ทันที
        threading.Thread(target=handle_incoming, args=(conn, addr), daemon=True).start()

# ============================================================
# 3. ส่งข้อความหาเพื่อนบ้าน (Forward Message)
# ============================================================
def forward_message(message, ttl, exclude=None):
    for peer_port in neighbor_table:
        # ข้ามเพื่อนที่เพิ่งส่งข้อความนี้มาให้เรา
        if peer_port == exclude:
            continue
            
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0) # ใส่ Timeout เผื่อเพื่อนตาย โปรแกรมจะได้ไม่ค้าง
            s.connect((HOST, peer_port))
            
            # โครงสร้าง Payload ใหม่: พอร์ตของเรา | TTL ปัจจุบัน | ข้อความ
            payload = f"{BASE_PORT}|{ttl}|{message}"
            s.sendall(payload.encode())
            s.close()
        except ConnectionRefusedError:
            print(f"[NODE {BASE_PORT}] Peer {peer_port} unreachable")
        except socket.timeout:
            print(f"[NODE {BASE_PORT}] Peer {peer_port} timeout")
        except Exception as e:
            print(f"[NODE {BASE_PORT}] Error sending to {peer_port}: {e}")

# ============================================================
# 4. การทำงานหลัก (Main)
# ============================================================
if __name__ == "__main__":
    # 1. เปิด Server ทิ้งไว้ใน Background
    threading.Thread(target=start_server, args=(BASE_PORT,), daemon=True).start()
    
    # 2. ส่งข้อความทักทายครั้งแรก
    test_message = f"Hello from node {BASE_PORT}"
    forward_message(test_message, TTL)
    
    # 3. ***จุดสำคัญ*** สร้าง Loop ไม่ให้โปรแกรมดับ และรอรับข้อความจากเราได้เรื่อยๆ
    print("-" * 50)
    print(f"Node {BASE_PORT} is active! Type a message to flood the network.")
    print("-" * 50)
    
    try:
        while True:
            # รับคำสั่งจากคีย์บอร์ด
            user_msg = input()
            if user_msg.strip(): # ถ้าไม่ได้พิมพ์แค่ช่องว่าง
                forward_message(user_msg, TTL)
    except KeyboardInterrupt:
        # กด Ctrl+C เพื่อออก
        print(f"\n[NODE {BASE_PORT}] Shutting down...")