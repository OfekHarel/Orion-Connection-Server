import socket

from utils import Networking

if __name__ == '__main__':
    s = socket.socket()
    s.connect(('127.0.0.1', 1690))
    msg = "APP!ID_VAL!1690!"
    Networking.send(s, msg)
    msg = ""
    done = False
    while not done:
        msg = Networking.receive(s)
        if msg is not "":
            print(msg)
            done = True

    Networking.send(s, Networking.assemble("SKIP"))


