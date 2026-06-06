# Name: WC_chat_server.py
# Purpose: Create a chat server
# Author: Core Python Programming - Wesley Chun
# Created: 11/04/2020
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

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while(True):
    try:

        print("[+] Waiting for connection...")
        tcpCliSock, addr = tcpSerSock.accept()
        print("[+] ...connected from: ", addr)

    except:
        print("[-] Conection close")
        break

    while(True):

        data = tcpCliSock.recv(BUFSIZ)

        if not data.decode():
            tcpCliSock.close()
            tcpSerSock.close()
            break

        time_stamp = ctime(time()).encode("UTF-8")
        separator = "-->".encode("UTF-8")
        tcpCliSock.send(time_stamp + separator)
        tcpCliSock.send(data)

















