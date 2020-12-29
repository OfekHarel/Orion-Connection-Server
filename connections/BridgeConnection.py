import socket

from utils import Networking
from utils.Networking import Operations


class BridgeConnection:
    def __init__(self, app: socket, computer: socket):
        self.app = app
        self.computer = computer

    def __str__(self):
        return "App Host: {} - Comp Host: {}".format(self.app.getpeername(), self.app.getpeername())

    def activate(self):
        msg = Networking.receive(self.app)
        if msg != "":
            if Networking.get_operation(msg) == Operations.DISCONNECT:
                return Operations.DISCONNECT

            else:
                Networking.send(self.computer, msg)

        msg = Networking.receive(self.computer)
        if msg != "":
            if Networking.get_operation(msg) == Operations.DISCONNECT:
                return Operations.DISCONNECT

            else:
                Networking.send(self.app, msg)

    def close(self):
        pass