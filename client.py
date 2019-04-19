from sys import argv
from pickle import dumps, loads
from socket import socket
from threading import Thread, RLock


class Client:
    def __init__(self, server_ip):
        self.name = 'Nameless'
        self.connected = False
        self.server_ip = server_ip
        self.new_messages = list()
        self.socket = None
        self.lock = RLock()

    def get_message(self):
        data_len = self.socket.recv(2)
        data = self.socket.recv(int.from_bytes(data_len, byteorder='big'))
        return loads(data)

    def send_message(self, message):
        packed = dumps(message)
        message = bytearray()
        message += len(packed).to_bytes(2, byteorder='big') + packed
        self.socket.send(message)

    def connect(self):
        self.update_thread = Thread(target=self.update_cycle)
        self.socket = socket()
        self.socket.connect((self.server_ip, 19001))
        self.connected = True
        self.send_message(self.name)

    def update_cycle(self):
        while self.connected:
            self.send_message('GetNewMessages')
            message = self.get_message()
            if message != 'NoNewMessages':
                with self.lock:
                    self.new_messages.append(message)

    def disconnect(self):
        self.connected = False
        self.update_thread.join()
        self.send_message('Disconnect')
        self.socket.close()


if __name__ == '__main__':
    if len(argv) == 1:
        CLIENT = Client('localhost')
    elif len(argv) == 2:
        CLIENT = Client(argv[1])
