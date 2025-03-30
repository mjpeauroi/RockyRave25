import socket
import pygame
import sys
from scipy.ndimage import gaussian_filter1d
import numpy as np

# --- Config ---
LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 5568
NUM_LEDS = 200
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 600

# --- UDP Setup ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))

# --- Pygame Setup ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hyperion LED Colors")

led_width = WINDOW_WIDTH // NUM_LEDS

print(f"Listening on {LISTEN_IP}:{LISTEN_PORT}...")

try:
    while True:
        # Handle window events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Receive data
        data, addr = sock.recvfrom(4096)
        expected_len = NUM_LEDS * 3
        if len(data) != expected_len:
            print(f"⚠️ Packet size mismatch: got {len(data)} bytes, expected {expected_len}")
            continue

        leds = np.frombuffer(data, dtype=np.uint8).reshape((NUM_LEDS, 3))
        # Apply Gaussian blur on each channel
        BLUR_SIGMA = 1
        rs = gaussian_filter1d(leds[:, 0], sigma=BLUR_SIGMA)
        gs = gaussian_filter1d(leds[:, 1], sigma=BLUR_SIGMA)
        bs = gaussian_filter1d(leds[:, 2], sigma=BLUR_SIGMA)

        # Draw colors
        screen.fill((0, 0, 0))
        for i in range(NUM_LEDS):
            r = rs[i]
            g = gs[i]
            b = bs[i]
            x = i * led_width
            pygame.draw.rect(screen, (r, g, b), (x, 0, led_width, WINDOW_HEIGHT))

        # # Draw colors
        # screen.fill((0, 0, 0))
        # for i in range(NUM_LEDS):
        #     r = data[i * 3]
        #     g = data[i * 3 + 1]
        #     b = data[i * 3 + 2]
        #     x = i * led_width
        #     pygame.draw.rect(screen, (r, g, b), (x, 0, led_width, WINDOW_HEIGHT))

        pygame.display.flip()
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    sock.close()
    pygame.quit()
