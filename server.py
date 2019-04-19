from socket import socket, timeout
from threading import Thread
from pickle import loads, dumps


class Chatter:
    def __init__(self, name, socket_, address):
        self.name = name
        self.socket = socket_
        self.address = address
        self.msgs = []


class Server:
    def __init__(self, ip, port):
        self.socket = socket()
        self.socket.settimeout(0.1)
        self.socket.bind((ip, port))
        self.socket.listen(2)
        self.chatters = []
        self.connect_thread = Thread(target=self.connect_cycle)
        self.connect_thread.start()
        print('started')

    def connect_cycle(self):
        while True:
            try:
                client, address = self.socket.accept()
            except timeout:
                continue

            client_name = self.get_message(client)
            for chatter in self.chatters:
                chatter.msgs.append('-> {} has connected.'.format(client_name))
            print('New chatter: {}'.format(client_name))
            new_chatter = Chatter(client_name, client, address)
            self.chatters.append(new_chatter)
            chatter_thread = Thread(target=self.chatter_work,
                                    args=(new_chatter,))
            chatter_thread.start()

    def chatter_work(self, chatter):
        while True:
            message = self.get_message(chatter.socket)
            if message == 'GetNewMessages':
                count = len(chatter.msgs)
                if count == 0:
                    self.send_message(chatter.socket, 'NoNewMessages')
                else:
                    for i in range(count):
                        self.send_message(chatter.socket,
                                          chatter.msgs.pop(0))
                continue

            if message == 'Disconnect':
                name = chatter.name
                self.chatters.remove(chatter)
                for man in self.chatters:
                    man.msgs.append('-> {} has disconnected.'.format(name))
                break

            for man in self.chatters:
                man.msgs.append('{}: {}'.format(chatter.name, message))

    @staticmethod
    def send_message(client, something):
        packed = dumps(something)
        message = bytearray()
        message += len(packed).to_bytes(2, byteorder='big') + packed
        client.send(message)

    @staticmethod
    def get_message(client):
        data_len = client.recv(2)
        data = client.recv(int.from_bytes(data_len, byteorder='big'))
        return loads(data)


if __name__ == '__main__':
    SERVER = Server('', 19001)
