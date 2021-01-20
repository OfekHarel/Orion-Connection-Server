import threading

from connections.Routine import Routine
from connections.SyncConnection import SyncConnection
import socket

from utils import Networking
from utils.DH_Encryption import Encryption


class BridgeConnection:
    """
    A bridge typed connection defines the flow connection between an app to a computer.
    """
    def __init__(self, app: socket, sync: SyncConnection, name: str, app_crypto: Encryption):
        self.app = app
        self.computer = sync.sock
        self.id = sync.id
        self.name = name
        self.comp_crypto = sync.crypto
        self.app_crypto = app_crypto
        self.is_active = False

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
        print("aaaaaaaaaaaaa")
        if not self.is_active:
            print("bbbbbbbbbbb")
            self.is_active = True
            t = threading.Thread(target=self.__app_bridge__())
            t.start()
            self.is_active = False

        if self.is_active:
            val = self.__comp_bridge__()

        return 1

    def __app_bridge__(self):
        while True:
            msg = Networking.receive(self.app, crypto=self.app_crypto)

            if msg is None:
                return
            elif msg != "":
                split = Networking.split(msg)
                if split[0] == self.name:
                    if Networking.get_disconnected(msg):
                        return

                    if split[1] == Networking.Operations.ROUTINE.value:
                        # split[2] - wanted time
                        # split[3] - time zone relative to GMT
                        # split[4] - ACTION
                        Routine(split[2], split[3], self.computer, self.app, split[4], self.comp_crypto).run()

                    else:
                        val = Networking.send(self.computer, Networking.assemble(split[1]), crypto=self.comp_crypto)
                        if not val:
                            return

    def __comp_bridge__(self):
        msg = Networking.receive(self.computer, crypto=self.comp_crypto)
        if msg is None:
            return 1
        elif msg != "":
            if Networking.get_disconnected(msg):
                return 2

            else:
                Networking.send(self.app, msg, crypto=self.app_crypto)

    def close(self):
        """
        This function will demolish a virtual bridge between the devices.
        """
        pass
