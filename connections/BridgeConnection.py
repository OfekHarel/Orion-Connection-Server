import threading

from connections.Routine import Routine
from connections.SyncConnection import SyncConnection
import socket

from data_base.Routines import Routines
from utils import Networking
from utils.DH_Encryption import Encryption
from utils.SmartThread import SmartThread


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
        self.is_active = True
        self.routines = Routines(name)

        self.com_proc = None
        self.app_proc = None

    def __str__(self):
        """
        A full description of the connection
        """
        return "\nApp Host: {}\nComp Host: {}\nName: {}".format(self.app.getpeername(), self.app.getpeername(),
                                                                self.name)

    def activate(self):
        """
        This function builds the virtual bridge between thr devices.
        This bridge allows flow of unsynchronized network transportation.
        If a msg in the bridge is the type of DISCONNECT it will return.
        """
        self.computer.setblocking(False)

        self.app_proc = SmartThread(self.__app_bridge__, "app")
        self.com_proc = SmartThread(self.__comp_bridge__, "computer")
        self.app_proc.start()
        self.com_proc.start()

        threading.Thread(target=self.is_running()).start()

    def __app_bridge__(self):
        try:
            is_done = False

            while not is_done:
                msg = Networking.receive(self.app, crypto=self.app_crypto)

                if msg is None:
                    is_done = True

                elif msg != "":
                    split = Networking.split(msg)
                    if split[0] == self.name:
                        if Networking.get_disconnected(msg):
                            self.routines.name = ""
                            is_done = True

                        if split[1] == Networking.Operations.ROUTINE.value:
                            # split[2] - wanted time
                            # split[3] - time zone relative to GMT
                            # split[4] - ACTION
                            # split[5] - name
                            self.routines.routines.append(Routine(split[2], split[3], self.computer, self.app,
                                                                  split[4], split[5], self.comp_crypto))

                        elif split[1] == Networking.Operations.DEL_ROUTINE.value:
                            # split[2] - name
                            for rout in self.routines.routines:
                                if rout.name == split[2]:
                                    rout.kill()
                                    self.routines.routines.remove(rout)
                        else:
                            val = Networking.send(self.computer, Networking.assemble(arr=split[1:]),
                                                  crypto=self.comp_crypto)
                            if not val:
                                is_done = True
        finally:
            pass

    def __comp_bridge__(self):
        try:
            is_done = False

            while not is_done:
                msg = Networking.receive(self.computer, crypto=self.comp_crypto)

                if msg is None:
                    is_done = True
                elif msg != "":
                    if Networking.get_disconnected(msg):
                        Networking.send(self.app, msg, crypto=self.app_crypto)
                        self.routines.name = ""
                        is_done = True
                    else:
                        Networking.send(self.app, msg, crypto=self.app_crypto)
        finally:
            pass

    def is_running(self):
        while self.app_proc.is_alive() and self.com_proc.is_alive():
            pass
        t = self.app_proc if self.app_proc.is_alive() else self.com_proc
        t.raise_exception()
        print(t.name + " aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        while t.is_alive():
            pass
        self.computer.setblocking(True)
