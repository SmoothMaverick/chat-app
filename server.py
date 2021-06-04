import socket
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created successfully")
except socket.error as err:
    print(f"Socket creation failed with error {err}")

port = 80
hostname = "www.google.com"

try:
    host_ip = socket.gethostbyname(hostname)
except socket.gaierror:
    print(f"there was an error resolving the {hostname}")
    sys.exit()

s.connect((host_ip, port))

print(f"The socket has successfully connected to {hostname}")
