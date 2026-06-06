# From Atreya
import socket
import sys


class CreateSocket():
    """ Main class that creates a Server socket """

    def __init__(self, host="localhost"):
        # Change to <target-ip> on production with different computers

        self.host = host
        self.port = 9999
        self.max_connections = 5

        try:

            self.sck = socket.socket()
            self.sck.bind((self.host, self.port))
            self.sck.listen(self.max_connections)

        except socket.error as msg:

            print(f"[-] Socket creation error: {msg}")

        print(f"[+] Server waiting for connections...")

    def socket_accept(self):
        """ Accept connections from clients """

        conn, address = self.sck.accept()
        print(
            f"[+] Connection has been established! ip: {address[0]} port:{address[1]}\n"
        )

        # Allows to send more than one command to the client
        self.send_command(conn)

        conn.close()

    def send_command(self, conn):
        """ Sending commands to the client """

        BUFFER_SIZE = 1024

        while True:
            # Allows to send more than one command to the client

            try:
                print("Enter command >> ", end="")
                cmd = input()

                # Close connection
                if cmd == "quit":
                    # Send it also to the client to close

                    conn.send(str.encode(cmd))
                    conn.close()
                    self.sck.close()
                    sys.exit()

                if len(str.encode(cmd)) > 0:
                    # The Server has entered a command

                    print(f"[+] Server asks: {cmd}")
                    conn.send(str.encode(cmd))
                    client_response = str(conn.recv(BUFFER_SIZE), "utf-8")
                    print(f"[+] Client says: {client_response}")
            except:
                print("[-] Error sending commands. Connection probably closed")
                conn.close()
                self.sck.close()
                sys.exit()


if __name__ == "__main__":
    sck = CreateSocket()
    sck.socket_accept()
