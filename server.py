import socket
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created successfully")
except socket.error as err:
    print(f"Socket creation failed with error {err}")

port = 12345

s.bind(("", port))
print(f"socket binded to {port}")
s.listen(5)
print("socket is listening")

while True:
    conn, addr = s.accept()
    print(f"Got connection from {addr}")
    conn.send(str.encode("Thank you for connecting"))
    conn.close()
