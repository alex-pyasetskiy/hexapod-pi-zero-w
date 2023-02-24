import socket
from threading import Thread
import json
import os
import sys

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

class TCPServer(Thread):
    ERROR = -1
    LISTEN = 1
    CONNECTED = 2
    STOP = 3

    SIG_NORMAL = 0
    SIG_STOP = 1
    SIG_DISCONNECT = 2

    def __init__(self, out_cmd_queue):
        Thread.__init__(self)

        self.cmd_queue = out_cmd_queue

        with open(f'{ROOT_DIR}/config.json', 'r') as read_file:
            self.config = json.load(read_file)
        
        self.host = socket.getfqdn()
        self.ip = '0.0.0.0'
        self.port = 9001
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.signal = self.SIG_NORMAL

    def run(self):
        try:
            self.tcp_socket.bind((self.ip, self.port))
        except socket.error as msg:
            print(f'# Bind failed. {msg} ')
            sys.exit()

        print('# Socket bind complete')

        # Start listening on socket
        self.tcp_socket.listen(10)
        print('# Socket now listening')

        # Wait for client
        conn, addr = self.tcp_socket.accept()
        print('# Connected to ' + addr[0] + ':' + str(addr[1]))

        # Receive data from client
        while True:     
            data = conn.recv(1024)
            line = data.decode('UTF-8')    # convert to string (Python 3 only)
            line = line.replace("\n","")   # remove newline character
            print( line )     

            if line:

                self.cmd_queue.put(line)
