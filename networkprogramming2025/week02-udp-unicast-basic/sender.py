import socket
import time
from config import HOST, PORT, BUFFER_SIZE

# 1. สร้าง UDP Socket (SOCK_DGRAM)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ตั้งค่า Timeout (เผื่อกรณีรอคำตอบจาก Server แล้วหายเงียบ)
sock.settimeout(5.0) 

print(f"--- UDP SENDER STARTED (Target: {HOST}:{PORT}) ---")
print("Type your message and press Enter. (Type 'exit' to quit)")

try:
    count = 1
    while True:
        # 2. รับข้อความจาก User
        user_input = input(f"[{count}] Enter message: ")
        
        if user_input.lower() == 'exit':
            break

        # 3. เตรียมข้อมูล (ใส่ Sequence Number และ Timestamp เข้าไปให้ดูเทพ)
        timestamp = time.strftime('%H:%M:%S')
        full_message = f"ID:{count} | Time:{timestamp} | Msg:{user_input}"
        
        # 4. ส่งข้อมูล (Fire and Forget)
        sock.sendto(full_message.encode(), (HOST, PORT))
        print(f"  >> Sent: {full_message}")

        # [Optionally] ลองรอ ACK สั้นๆ (ถ้าฝั่ง Receiver เขียนให้ส่งกลับมา)
        # try:
        #     data, addr = sock.recvfrom(BUFFER_SIZE)
        #     print(f"  << Server ACK: {data.decode()}")
        # except socket.timeout:
        #     print("  !! No ACK received (Normal for standard UDP)")

        count += 1

except KeyboardInterrupt:
    print("\n[SENDER] Interrupted by user.")

finally:
    print("[SENDER] Closing socket...")
    sock.close()