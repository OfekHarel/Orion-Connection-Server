import socket


class SyncConnection:
    def __init__(self, sock: socket, id_num: str):
        self.sock = sock
        self.id = id_num

    def __str__(self):
        return "Host: {} - ID: {}".format(self.sock.getpeername(), self.id)
