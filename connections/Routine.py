import threading
import time
import datetime
import pytz

from socket import socket

from utils import Networking


class Routine:
    def __init__(self, wanted_time: str, time_zone: str, computer: socket, app: socket, msg: str):
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
        self.name = msg[0]
        self.msg = msg[1]

        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        sent = False
        while self.is_run:
            time_z = datetime.datetime.now(pytz.timezone('Zulu'))
            c_time = time_z.strftime("%H:%M")
            while self.is_run and (c_time != self.time):
                sent = False
                time.sleep(6)
                c_time = time_z.strftime("%H:%M")

            if self.is_run and (c_time == self.time) and (not sent):
                Networking.send(self.comp, Networking.assemble(self.msg))
                Networking.send(self.app, Networking.assemble(Networking.Operations.ROUTINE.value, self.name))

                time.sleep(40)
                sent = True
