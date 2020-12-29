from socket import socket

from data_base.DataTools import Devices
from utils.Enum import Enum

SEP = '!'
HEADER = 3


def split(msg: str):
    msg = msg.split('!')
    return msg[:len(msg) - 1]


def get_operation(msg: str):
    msg = split(msg)
    return Operations.DISCONNECT if msg[0] == Operations.DISCONNECT.value else None


def sync_msg(msg: str):
    msg = split(msg)
    dev = Devices.COMPUTER if msg[0] == Devices.COMPUTER.value else Devices.APP
    id_num = msg[2]
    return dev, id_num


def send(sock: socket, msg: str):
    size = str(len(msg)).zfill(HEADER)
    sock.send(bytes(size.encode()))
    sock.send(msg.encode())


def receive(sock: socket):
    try:
        size = int(str(sock.recv(HEADER).decode()))
        req = sock.recv(size + 1)
        return req.decode()

    except Exception as e:
        print(e.__traceback__)


def assemble(*msg: str):
    final = ''
    for request in msg:
        final += "{}{}".format(request, SEP)

    return final


class Operations(Enum):
    INVALID = "INVALID"
    VALID = "VALID"
    DISCONNECT = "DICON"
