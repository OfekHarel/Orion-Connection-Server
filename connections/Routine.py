import threading
import time
import datetime
from utils.DH_Encryption import Encryption
import pytz

from socket import socket

from utils import Networking


class Routine:
    def __init__(self, wanted_time: str, time_zone: str, computer: socket, app: socket, msg: str, crypto: Encryption):
        time_formatted = wanted_time.split(":")
        h_zone = time_zone[1:3]
        m_zone = time_zone[3:]
        sign = -1 if time_zone[0] == "+" else 1
        w_h = time_formatted[0]
        w_m = time_formatted[1]
        h = (int(h_zone) * sign) + int(w_h)
        m = (int(m_zone) * sign) + int(w_m)

        self.time = str(datetime.time(h, m))[:5]
        self.comp = computer
        self.app = app
        self.is_run = True
        self.msg = msg
        self.crypto

        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        sent = False
        while self.is_run:
            c_time = self.update_time()
            while self.is_run and (c_time != self.time):
                sent = False
                time.sleep(6)
                c_time = self.update_time()

            if self.is_run and (c_time == self.time) and (not sent):
                Networking.send(self.comp, Networking.assemble(self.msg), crypto=self.crypto)
                time.sleep(60)
                sent = True

    def update_time(self):
        time_z = datetime.datetime.now(pytz.timezone('Zulu'))
        return time_z.strftime("%H:%M")
