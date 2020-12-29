import socket

from utils import Networking

if __name__ == '__main__':
    s = socket.socket()
    s.connect(('127.0.0.1', 1690))
    msg = "APP!ID_VAL!3339!"
    Networking.send(s, msg)
    msg = ""
    done = False
    while not done:
        msg = Networking.receive(s)
        if msg is not "":
            print(msg)
            done = True

    msg = ""
    done = False
    while not done:
        msg = Networking.receive(s)
        if msg is not "":
            print(msg)
            done = True


