import socket
import time

# --- Hyperion Configuration ---
LISTEN_IP = "0.0.0.0"      # Listen on all interfaces
LISTEN_PORT = 5568         
NUM_LEDS = 200             
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_sock.bind((LISTEN_IP, LISTEN_PORT))
print(f"Listening for Hyperion UDP packets on {LISTEN_IP}:{LISTEN_PORT}...")

# --- QTPY Configuration ---
QT_PY_IP = "192.168.0.54" 
QT_PY_PORT = 4210
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# --- Main loop ---
i = 0
try:
    while True:
        data, addr = recv_sock.recvfrom(4096)  # Max size > expected packet
        expected_len = NUM_LEDS * 3
        if len(data) != expected_len:
            print(f"?? Packet size mismatch: got {len(data)} bytes, expected {expected_len}")
            continue
        send_sock.sendto(data, (QT_PY_IP, QT_PY_PORT))
        print(f"Sent and recieved {i}")
        i += 1
        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    send_sock.close()
    recv_sock.close()


