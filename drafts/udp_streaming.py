import socket
import time

# --- Configuration ---
LISTEN_IP = "0.0.0.0"      # Listen on all interfaces
LISTEN_PORT = 5568         
NUM_LEDS = 200             


# frequency is 25.003969554478427
# --- Set up socket ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))

print(f"Listening for Hyperion UDP packets on {LISTEN_IP}:{LISTEN_PORT}...")
# N = 1000
# t0 = time.time()
try:
    while True:
    # for _ in range(N):
        data, addr = sock.recvfrom(4096)  # Max size > expected packet
        # print(data)
        # print('\n')
        # print(type(data))
        # print('\n')
        # print(len(data))
        # print('\n')
        # print(addr)
        # break
        expected_len = NUM_LEDS * 3
        # print(data)
        # print(addr)
        # break
        if len(data) != expected_len:
            print(f"?? Packet size mismatch: got {len(data)} bytes, expected {expected_len}")
            continue

        # Parse RGB values
        leds = []
        for i in range(NUM_LEDS):
            r = data[i * 3]
            g = data[i * 3 + 1]
            b = data[i * 3 + 2]
            leds.append((r, g, b))

        print(f"Received {len(leds)} LEDs from {addr[0]}:{addr[1]} | 30th LED: {leds[30]}")

    # t1 = time.time()
    # print(f"frequency is {N/(t1-t0)}")
except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    sock.close()
