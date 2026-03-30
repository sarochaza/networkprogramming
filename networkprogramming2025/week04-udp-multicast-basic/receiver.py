import socket
import struct
from config import MULTICAST_GROUP, PORT, BUFFER_SIZE

# สร้าง UDP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)


sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(("", PORT))

# Join Multicast Group (การบอก Kernel ให้รับข้อมูลจากกลุ่มนี้)
mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print(f"[RECEIVER] Joined {MULTICAST_GROUP}:{PORT}")
print("Waiting for multicast messages...")

try:
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        print(f"[RECEIVER] {addr} -> {data.decode()}")
except KeyboardInterrupt:
    print("\n[RECEIVER] Leaving group...")
finally:
    # ยกเลิกการเป็นสมาชิกกลุ่มก่อนปิด (Good practice)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
    sock.close()