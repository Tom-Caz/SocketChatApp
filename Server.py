import socket
from socket import *
from random import randint
import threading

users = {}


# Starts the server
def runServer():
    server_port = 12000
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen()
    print("The server is ready to receive...")
    while True:  # Accepts new users
        connection_socket, addr = server_socket.accept()
        username = 'User{}'.format(str(randint(1000, 9999)))
        while username in users.values():  # Checks if random username already exists
            username = 'User{}'.format(str(randint(1000, 9999)))
        users[connection_socket, addr] = username
        sendConnMsg(connection_socket, addr)
        displayUsers(connection_socket, addr)
        threading.Thread(target=recvMsg, args=[server_socket, connection_socket,
                                               addr]).start()  # Creates a thread to receive messages from clients


# Receives messages from clients
def recvMsg(server_socket, connection_socket, addr):
    msgUser = connection_socket, addr
    try:
        while True:
            msg = connection_socket.recv(1024)
            if msg:
                if msg.decode() == '.exit':
                    connection_socket.close()
                    msgUserName = users[msgUser]
                    users.pop(msgUser)
                    sendDisconMsg(msgUserName)
                else:
                    sendMsg(msg, msgUser)  # Sends message to all users connected to server
            else:
                break
    except:
        connection_socket.close()
        users.pop(connection_socket, addr)
        print('User Disconnected')
    connection_socket.close()
    users.pop(connection_socket, addr)


def sendConnMsg(connection_socket, addr):
    for user in users:
        if user != (connection_socket, addr):
            user[0].send(str.encode("{} has joined.".format(users[connection_socket, addr])))


# Sends messages to clients
def sendMsg(msg, msgUser):
    for user in users:
        to_send = str.encode(users[msgUser] + ": " + msg.decode())
        user[0].send(to_send)


def sendDisconMsg(msgUser):
    disconMsg = str.encode("{} has disconnected.".format(msgUser))
    for user in users:
        print(users[user])
        user[0].send(disconMsg)


def displayUsers(connection_socket, addr):
    to_send = "Users Connected:"
    for user in users:
        to_send += '\n' + users[user]
    to_send += "\t(You)"
    connection_socket.send(str.encode(to_send))


if __name__ == "__main__":
    runServer()
