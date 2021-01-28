import threading
import socket

from connections.BridgeConnection import BridgeConnection
from connections.SyncConnection import SyncConnection
from data_base.DataTools import DataTools
from data_base.DataBase import DataBase
from data_base.DataTools import Devices
from utils import Networking, DH_Encryption
from utils.DH_Encryption import Encryption
from utils.Networking import Operations


class BridgeServer:
    """
    A class to represent a server that it's job is to be a "bridge" between the devices.
    To transfer a msg from one device to the other.
    """
    def __init__(self):
        self.server_sock = socket.socket()
        self.server_sock.bind(('', 1691))
        self.server_sock.listen(20)

        self.data = DataBase()
        self.dataTools = DataTools(self.data)

    def go_crypto(self, sock: socket) -> Encryption:
        g = DH_Encryption.generate_prime()
        n = DH_Encryption.generate_n()
        crypto = Encryption(g, n)
        Networking.send(sock, Networking.assemble(Networking.Operations.CONNECT.value, str(g), str(n),
                                                  str(crypto.get_partial_key())))
        g_pow_b_mod_n = int(Networking.split(Networking.receive(sock))[1])
        crypto.get_full_key(g_pow_b_mod_n)
        return crypto

    def __sync__(self, sock: socket, crypto: Encryption):
        """
            Sync phase of each type of device.
        """
        synced = False, None
        done = False
        while not done:
            msg = Networking.receive(sock, crypto=crypto)
            if msg is not None:
                dev, id_num = Networking.sync_msg(msg)

                if dev is Devices.COMPUTER:  # if a computer is trying to connect
                    sync_conn = SyncConnection(sock, id_num, crypto)
                    if self.dataTools.is_id_valid(Devices.COMPUTER, id_num):
                        self.data.add(sync=sync_conn)
                        msg = Networking.assemble(Operations.VALID.value)
                        Networking.send(sock, msg, crypto=crypto)
                        done = True
                        continue

                    else:
                        msg = Networking.assemble(Operations.INVALID.value)
                        Networking.send(sock, msg, crypto=crypto)

                elif dev is Devices.APP:  # if an app is trying to connect
                    if self.dataTools.is_id_valid(Devices.APP, id_num):
                        Networking.send(sock, Networking.assemble(Operations.VALID.value), crypto=crypto)
                        name = Networking.split(Networking.receive(sock, crypto=crypto))[0]
                        comp = self.dataTools.find(id_num)
                        bridge = BridgeConnection(sock, comp, name, crypto)
                        self.data.add(bridge=bridge)
                        self.data.remove(sync=comp)
                        synced = True, bridge
                        done = True
                        continue
                    else:
                        msg = Networking.assemble(Operations.INVALID.value)
                        Networking.send(sock, msg, crypto=crypto)
                        done = True
                        continue
        return synced

    def __manage__(self):
        """
          This function is responsible of accepting new connections and transferring
          them throw the sync phase till the bridge phase
       """
        sock, address = self.server_sock.accept()

        self.dataTools.is_pair_gone()

        synced, bridge = self.__sync__(sock, self.go_crypto(sock))
        if synced:
            t = threading.Thread(target=self.__bridge__, args=(bridge, address))
            t.start()

    def __bridge__(self, bridge: BridgeConnection, address):
        """
            The bridge phase. Main phase of each socket, where the communication is happening.
        """
        Networking.send(bridge.computer, Networking.assemble(Networking.Operations.PAIRED.value),
                        crypto=bridge.comp_crypto)
        specs = Networking.split(Networking.receive(bridge.computer, crypto=bridge.comp_crypto))
        print(str(specs) + "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        specs[0] = Networking.Operations.PAIRED.value
        Networking.send(bridge.app, Networking.assemble(arr=specs), crypto=bridge.app_crypto)
        
        dis = None
        while dis is None:
            dis = bridge.activate()

        self.data.add(sync=SyncConnection(bridge.computer, bridge.id, bridge.comp_crypto))
        bridge.com_proc.terminate()
        self.data.remove(bridge=bridge)

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
