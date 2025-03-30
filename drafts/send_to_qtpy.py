import socket
import time

# --- Config ---
QT_PY_IP = "192.168.0.54" 
QT_PY_PORT = 4210

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
i = 0
try:
    while True:
        message = f"Hello QtPy! {i}"
        sock.sendto(message.encode(), (QT_PY_IP, QT_PY_PORT))
        print(f"Sent: {message}")
        time.sleep(1/25)  # 25 Hz
        i += 1
except KeyboardInterrupt:
    print("\nStopping sender...")
finally:
    sock.close()
