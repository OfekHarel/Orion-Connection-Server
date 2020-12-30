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
    """
    A class to represent a server that it's job is to be a "bridge" between the devices.
    To transfer a msg from one device to the other.
    """
    def __init__(self):
        self.server_sock = socket.socket()
        self.server_sock.bind(('', 1690))
        self.server_sock.listen(20)

        self.data = DataBase()
        self.dataTools = DataTools(self.data)

    def __sync__(self, sock: socket):
        """
            Sync phase of each type of device.
        """
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

        elif dev is Devices.APP:  # if an app is trying to connect
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

    def __manage__(self):
        """
          This function is responsible of accepting new connections and transferring
          them throw the sync phase till the bridge phase
       """
        sock, address = self.server_sock.accept()
        synced, bridge = self.__sync__(sock)

        if synced:
            t = threading.Thread(target=self.__bridge__, args=(bridge, address))
            t.start()

    def __bridge__(self, bridge, address):
        """
            The bridge phase. Main phase of each socket, where the communication is happening.
        """
        is_done = False

        while not is_done:
            is_done = bridge.activate()
            if is_done == Operations.DISCONNECT:
                is_done = True

        self.data.remove(bridge_connection=bridge)

    def run(self):
        """
           The main server_sock function - This function runs the server_sock.
        """
        while True:
            print(self.data)
            self.__manage__()


if __name__ == '__main__':
    server = BridgeServer()
    server.run()

    server.server_sock.close()
