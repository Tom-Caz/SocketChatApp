from socket import *
import threading


# Starts the client. Connects to the server
def runClient():
    server_name = ''
    server_port = 12000
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    print("Connected. Enter you message to send:            ('.exit' to exit)")
    threading.Thread(target=recvMsg, args=[client_socket]).start()  # Starts a new thread to receive messages
    sendMsg(client_socket)
    client_socket.close()


# Sends message to server
def sendMsg(client_socket):
    msg = ""
    while msg != ".exit":
        msg = input()
        client_socket.send(str.encode(msg))


# Receives messages from the server
def recvMsg(client_socket):
    try:
        while True:
            recvdMsg = client_socket.recv(1024)
            plainTextMsg = recvdMsg.decode()
            print(plainTextMsg)
    except:
        print("Client closed")


if __name__ == "__main__":
    runClient()
