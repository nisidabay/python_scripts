# Name: WC_chat_client.py
# Purpose: Create a chat client
# Author: Core Python Programming - Wesley Chun
# Created: 12/04/2020
# Version: 1.0
# Changes:Need to be revised


from socket import *
from time import time, ctime

# On different machines the HOST must be the
# IP of the server
HOST = "localhost"
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while(True):
    data = input("[+] -> ")

    if not data:
        break
    tcpCliSock.send(data.encode("UTF-8"))
    data = tcpCliSock.recv(BUFSIZ)
    if not data:
        break
    print(data)

tcpCliSock.close()














