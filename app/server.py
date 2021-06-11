import socket
import select
import sys

import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

addr = "localhost"
port = 12345

server.bind((addr, port))

server.listen(100)

print(f"Server listening on {addr}:{port}")

clients_list = []


def clientthread(conn, addr):
    conn.send(str.encode("Welcome to the chat room!"))

    while True:
        try:
            message = conn.recv(2048)

            if message:
                print(f"< {addr[0]} > {message}")

                message_to_send = f"< {addr[0]} > {message}"
                broadcast(message_to_send, conn)
            else:
                remove(conn)
        except Exception as err:
            print(f"Error: {err}")
            continue


def broadcast(mess, conn):
    for client in clients_list:
        if client != conn:
            try:
                client.send(str.encode(mess))
            except:
                client.close()
                remove(client)


def remove(conn):
    if conn in clients_list:
        clients_list.remove(conn)


while True:
    conn, addr = server.accept()
    clients_list.append(conn)

    print(f"{addr[0]} connected")

    thread = threading.Thread(target=clientthread, args=[conn, addr])
    thread.start()

conn.close()
server.close()
