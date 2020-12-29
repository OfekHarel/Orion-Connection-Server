import socket


class SyncConnection:
    """
    A sync typed connection defines the pairing between each computer to it's app.
    """
    def __init__(self, sock: socket, id_num: str):
        self.sock = sock
        self.id = id_num

    def __str__(self):
        """
        A full description of the connection
        """
        return "Host: {} - ID: {}".format(self.sock.getpeername(), self.id)
