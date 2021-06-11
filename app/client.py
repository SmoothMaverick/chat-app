import socket
import select
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

addr = "localhost"
port = 12345

client.connect((addr, port))

while True:
    sockets_list = [sys.stdin, client]

    read_sockets, write_sockets, error_sockets = select.select(sockets_list, [], [])

    for socks in read_sockets:
        if socks == client:
            message = socks.recv(2048)
            print(str(message))
        else:
            message = sys.stdin.readline()
            client.send(str.encode(message))
            sys.stdout.write("<You>")
            sys.stdout.write(message)
            sys.stdout.flush()

client.close()
