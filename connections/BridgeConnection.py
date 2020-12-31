from connections.SyncConnection import SyncConnection
import socket

from utils import Networking
from utils.Networking import Operations, split


class BridgeConnection:
    """
    A bridge typed connection defines the flow connection between an app to a computer.
    """
    def __init__(self, app: socket, sync: SyncConnection, name: str):
        self.app = app
        self.computer = sync.sock
        self.id = sync.id
        self.name = name

    def __str__(self):
        """
        A full description of the connection
        """
        return "\nApp Host: {}\nComp Host: {}\nName: {}".format(self.app.getpeername(), self.app.getpeername(), self.name)

    def activate(self):
        """
        This function builds the virtual bridge between thr devices.
        This bridge allows flow of unsynchronized network transportation.
        If a msg in the bridge is the type of DISCONNECT it will return.
        :return: DISCONNECT if it occurred.
        """
        msg = Networking.receive(self.app)
        if msg is None:
            print("none")
            return
        elif msg != "":
            split = Networking.split(msg)
            if split[0] == self.name:
                if Networking.get_disconnected(msg) == Operations.DISCONNECT:
                    return Operations.DISCONNECT

                else:
                    Networking.send(self.computer, Networking.assemble(split[1]))

        msg = Networking.receive(self.computer)
        if msg is None:
            return Operations.DISCONNECT
        elif msg != "":
            if Networking.get_disconnected(msg) == Operations.DISCONNECT:
                return Operations.DISCONNECT

            else:
                Networking.send(self.app, msg)

    def close(self):
        """
        This function will demolish a virtual bridge between the devices.
        """
        pass
