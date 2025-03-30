import socket
import json
import time

ip = "192.168.0.83"  # Replace with your Hyperion server IP
port = 19444  # TCP (JSON Server) port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to Hyperion
sock.connect((ip, port))
print("Connected to Hyperion JSON Server")

# Send a request for LED colors
request = {
    "command": "ledcolors",
    "subcommand": "ledstream-start",
}
sock.sendall((json.dumps(request) + "\n").encode('utf-8'))


'''
Notes about receiveing time:
when leds are all zero, the size is 1284 
    with buffer size 4096 the frequency is 10.06930101045098
the average size when watching white lotus is 2233 bytes with frequency 10.13
the average size when watching himym is 1644 bytes with frequency 9.05
'''
# Receive the response
lengths = []

N=1000
t0 = time.time()
for _ in range(N):
    try:
        response = sock.recv(4096)  # Adjust buffer size if needed
        lengths.append(len(response))
        # print("size is " + str(len(response)))
        # # print("Received:", response.decode('utf-8'))
        # decodedresponse = json.loads(response.decode('utf-8'))
        # print(decodedresponse["result"]["leds"])
    except:
        print("fail, try again")
t1 = time.time()
print(f"N = {N}")
print(f"frequency {N/(t1-t0)}")
print(f"avg length {sum(lengths)/len(lengths)}")
sock.close()

