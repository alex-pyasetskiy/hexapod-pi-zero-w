import socket
from threading import Thread
import json
from hex_server import ROOT_DIR

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
            self.tcp_socket.listen(1)
            print(f'TCP listening {self.ip}')
        except OSError as err:
            # print('emit tcp server error')
            # self.status.emit(self.STOP, '')
            pass
        else:
            while True:
                self.cmd_queue.put('standby:')
                # Wait for a connection
                # print('wait for a connection')
                # self.status.emit(self.LISTEN, '')
                try:
                    self.connection, addr = self.tcp_socket.accept()
                    # self.connection.setblocking(False)
                    # self.connection.settimeout(1)
                    print('New connection')
                except socket.timeout as t_out:
                    pass
                else:
                    while True:
                        # print('waiting for data')
                        # if self.signal == self.SIG_NORMAL:
                        try:
                            data = self.connection.recv(4096)
                        except socket.error as e:
                            print(e)
                            break
                        else:
                            if data:
                                self.cmd_queue.put(data.decode())
                            else:
                                break

        finally:
            self.tcp_socket.close()
            self.cmd_queue.put('standby:')
            print('exit')
