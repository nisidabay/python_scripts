# Name: chat-server.py
# Purpose: Create a chat server
# Author: Bhaskar Chaudhary - Tkinter GUI Application Development Blueprints
# Created: 17/03/2020
# Version: 1.0
# Changes:Need to be revised

import socket
import threading
import sys
import pickle


class Servidor:
    """ Main class that creates a socket on the Server.
        Messages are serialized
    """

    def __init__(self):

        self.host = socket.gethostname()
        self.port = 9999
        self.clientes = []
        MAX_CONNECTIONS = 5

        try:

            self.sck = socket.socket()
            self.sck.bind((self.host, self.port))
            self.sck.listen(MAX_CONNECTIONS)
            self.sck.setblocking(True)

            shutdown = False

            accept_conn = threading.Thread(target=self.accept_conn)
            process_conn = threading.Thread(target=self.process_conn)

            accept_conn.daemon = True
            accept_conn.start()

            process_conn.daemon = True
            process_conn.start()

            print("[+] Server online:\nsalir -> Cierra el chat.")
            while not shutdown:
                
                msg = input("[+] Server says -> ")

                if msg == "salir":
                    self.closing_msg()
                    self.sck.close()
                    sys.exit()
                    shutdown = True

        except:
            pass

    def accept_conn(self):
        """ Accepts connections from the clients """

        while True:
            try:

                conn, addr = self.sck.accept()
                conn.setblocking(True)
                # Add client to list
                self.clientes.append(conn)

                print(f"[+] Connection has been established: {addr[0]}: ", end="")
                print(f"{len(self.clientes)} clients connected")
                
            except:
                pass

    def process_conn(self):
        """ Proccess the data received from clients
            and spread out the message
        """
        while True:
            if len(self.clientes) > 0:
                for cliente in self.clientes:
                    
                    try:

                        data = cliente.recv(1024)
                        if data != "salir":
                            print(f"[+] Client {client.gethostname()} says -> {data}")
                            print(pickle.loads(data))
                            self.msg_to_all(data)
                            
                        else:
                            
                            print(pickle.loads(data))
                            self.msg_to_all(data)

                            self.closing_msg()
                            self.sck.close()
                            sys.exit()

                    except:
                        pass

    def msg_to_all(self, msg):
        """ Send messages to everyone but the sender """

        c.send(pickel.dumps(msg))
        for c in self.clientes:
            try:

               # if c != cliente:
                c.send(pickel.dumps(msg))

            except:
                """ the client is not online """
                self.clientes.remove(c)

    def closing_msg(self):
        """ Telling clients the chat is closed """

        for cliente in self.clientes:
            cliente.send(pickle.dumps("""
            Server says: The chat is closed.
            Clients should close connection
            by entering: salir"""
                                      ))


if __name__ == "__main__":
    s = Servidor()

















