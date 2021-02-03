from socket import socket
from data_base.DataTools import Devices
from utils.Enum import Enum

SEP = '!'
HEADER = 4


def split(msg: str):
    """
    This function will split the msg to a list according to the separator char.
    :param msg: A raw msg from network to split.
    :return: A list when each index contains a part of the msg.
    """
    try:
        msg = msg.split('!')
        return msg[:len(msg) - 1]
    except AttributeError:
        pass


def get_disconnected(msg: str):
    """
    This function will find if the msg contains a DISCONNECTED operation
    :param msg: A raw msg from network.
    :return: None or DISCONNECTED according to the msg
    """
    msg = split(msg)
    return msg[0] == Operations.DISCONNECT.value


def sync_msg(msg: str):
    """
    This function will handle any sync type msg and obtain from it the wanted info
    :param msg: A raw msg from network.
    :return: The type of the device and the id from the msg
    """
    msg = split(msg)
    dev = Devices.COMPUTER if msg[0] == Devices.COMPUTER.value else Devices.APP
    id_num = msg[2]
    return dev, id_num


def send(sock: socket, msg: str, crypto=None) -> bool:
    """
    :param crypto:
    :param sock: The network socket to send from.
    :param msg: The protocol based msg.
    """
    try:
        if crypto is not None:
            size = str(len(msg) * 4).zfill(HEADER)
            sock.send(bytes(size.encode("UTF-8")))
            msg = crypto.encrypt_message(msg)
            sock.send(msg.encode("UTF-16LE"))
            print("send {}->{}".format(size, crypto.decrypt_message(msg)))

        else:
            size = str(len(msg)).zfill(HEADER)
            sock.send(bytes(size.encode("UTF-8")))
            sock.send(msg.encode("UTF-8"))
            print("send {}->{}".format(size, msg))

        return True

    except ValueError:
        return True

    except Exception:
        return False


def receive(sock: socket, crypto=None) -> str or None:
    """
    :param crypto:
    :param sock: The network socket to receive from.
    :return: The raw decoded msg from the network.
    """
    try:
        size = int(str(sock.recv(HEADER).decode("UTF-8", "ignore")))
        print(size)
        msg = sock.recv(size)
        if crypto is not None:
            msg = crypto.decrypt_message(msg.decode("UTF-16LE", "ignore"))
            print(msg)
        else:
            msg = msg.decode("UTF-8", "ignore")
        print("recv " + msg)
        return msg

    except OSError or ValueError:
        return ""

    except Exception as e:
        print(e)
        return None


def assemble(*msg: str, arr=None):
    """
    This function will create a string that follows the protocol.
    :param arr:
    :param msg: Strings to create the protocol string
    :return: The full protocol string
    """
    print(msg)
    final = ''
    if arr is None:
        for request in msg:
            final += "{}{}".format(request, SEP)
    else:
        for msg in arr:
            final += "{}{}".format(msg, SEP)

    return final


class Operations(Enum):
    """
    Any operation that the server can send or do.
    """
    INVALID = "INVALID"
    VALID = "VALID"
    DISCONNECT = "DISCON"
    PAIRED = "HELLO"
    ROUTINE = "ROUT"
    CONNECT = "CONN"
    DEL_ROUTINE = "DROUT"
