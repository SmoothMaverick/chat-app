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
nicknames_set = set()


class Client:
    def __init__(self, nickname: str, conn):
        self.nickname = nickname
        self.conn = conn

     def set_nickanem():
         pass


def clientthread(client, addr):
    client.conn.send(str.encode("Welcome to the chat room!"))
    client.conn.send(str.encode("What is your nickname?"))
    nickname = ""
    isNicknameSet = False

    while True:
        try:
            message = client.conn.recv(2048)

            # handle_nickname()
            # TODO: what if "\n"
            if nickname == "":
                nickname = message

                if nickname in nicknames_set:
                    message_to_send = "ERROR: nickname is already taken"
                    client.conn.send(str.encode(message_to_send))
                    nickname = ""
                elif nickname == "":
                    message_to_send = "ERROR: nickname cannot be empty"
                    client.conn.send(str.encode(message_to_send))
                else:
                    nicknames_set.add(nickname)

                client.nickname = nickname

            if nickname == "":
                continue

            if isNicknameSet == False and nickname != "":
                isNicknameSet = True
                otherClientNicknames = []

                for otherClient in clients_list:
                    if otherClient.conn != client.conn:
                        otherClientNicknames.append(otherClient.nickname)

                otherClientsCount = len(otherClientNicknames)

                if otherClientsCount == 0:
                    client.conn.send(str.encode(f"You are the first person to connect"))
                else:
                    client.conn.send(
                        str.encode(
                            f"You are connected with {otherClientsCount} other users with {otherClientNicknames}"
                        )
                    )

                continue

            if message:
                print(f"< {client.nickname} > {message.decode('utf-8')}")

                message_to_send = f"< {client.nickname} > {message.decode('utf-8')}"
                broadcast(message_to_send, client.conn)
            else:
                message_to_send = f"{client.nickname} has left the chat"
                broadcast(message_to_send, client.conn)
                remove(client)
                break
        except Exception as err:
            print(f"Error: {err}")
            continue


def broadcast(mess, conn):
    for client in clients_list:
        if client.conn != conn:
            try:
                client.conn.send(str.encode(mess))
            except:
                client.conn.close()
                remove(client)


def remove(client):
    if client in clients_list:
        clients_list.remove(client)


while True:
    conn, addr = server.accept()
    newClient = Client("", conn)
    clients_list.append(newClient)

    print(f"{addr[0]} connected")

    thread = threading.Thread(target=clientthread, args=[newClient, addr])
    thread.start()

# conn.close()
# server.close()
