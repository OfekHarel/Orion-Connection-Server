import threading
import socket

from connections.BridgeConnection import BridgeConnection
from connections.SyncConnection import SyncConnection
from data_base.DataTools import DataTools
from data_base.DataBase import DataBase
from data_base.DataTools import Devices
from utils import Networking
from utils.Networking import Operations


class BridgeServer:
    def __init__(self):
        self.server = socket.socket()
        self.server.bind(('', 1690))
        self.server.listen(20)

        self.data = DataBase()
        self.dataTools = DataTools(self.data)

    def __sync__(self, sock: socket):
        dev, id_num = Networking.sync_msg(Networking.receive(sock))
        msg = None
        synced = False, None

        if dev is Devices.COMPUTER:  # if a computer is trying to connect
            sync_conn = SyncConnection(sock, id_num)
            if self.dataTools.is_id_valid(Devices.COMPUTER, id_num):
                self.data.add(sync_connection=sync_conn)
                msg = Networking.assemble(Operations.VALID.value)
            else:
                msg = Networking.assemble(Operations.INVALID.value)

        elif dev is Devices.APP:  # if a mobile is trying to connect
            if self.dataTools.is_id_valid(Devices.APP, id_num):
                comp = self.dataTools.find(id_num)
                bridge = BridgeConnection(sock, comp.sock)

                self.data.add(bridge_connection=bridge)
                self.data.remove(sync_connection=comp)

                msg = Networking.assemble(Operations.VALID.value)
                synced = True, bridge
            else:
                msg = Networking.assemble(Operations.INVALID.value)

        Networking.send(sock, msg)
        return synced

    def accept(self):
        sock, address = self.server.accept()
        synced, bridge = self.__sync__(sock)

        if synced:
            t = threading.Thread(target=self.bridge, args=(bridge, address))
            t.start()

    def bridge(self, bridge, address):
        is_done = False

        while not is_done:
            is_done = bridge.activate()
            if is_done == Operations.DISCONNECT:
                self.data.connections.remove(bridge)
                is_done = True


    def run(self):
        while True:
            print(self.data.__str__())
            self.accept()


if __name__ == '__main__':
    server = BridgeServer()

    server.run()
    server.server.close()
