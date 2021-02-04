from data_base.DataBase import DataBase
from data_base.Routines import Routines
from utils import Networking
from utils.Enum import Enum


class Devices(Enum):
    """
    Enum to represent the devices types that can connect to the server.
    """
    APP = "APP"
    COMPUTER = "COMPUTER"


class DataTools:
    """
    Util class for tools to use on the database.
    """
    def __init__(self, base: DataBase):
        self.base = base

    def is_id_valid(self, device: Devices, id_num: str):
        """
        This function will check if the ID is valid according to the type of the device.
        If it's an app it will check if there is an ID that matches this ID.
        If it's a computer software it will check if there is not an ID that matches this ID.
        :param device: The type of device - according to this param the validation process wil change.
        :param id_num:
        :return: whether the ID is valid according to the device.
        """
        for c in self.base.sync_connections:
            if c.id == id_num:
                return device == Devices.APP
        return device == Devices.COMPUTER

    def find(self, id_num: str):
        """
        This function finds a Sync connection according to an ID.
        :param id_num: The ID that matches the Sync Connection to find.
        :return: Sync connection - if there isn't - None.
        """
        for c in self.base.sync_connections:
            if c.id == id_num:
                return c

        return None

    def is_pair_gone(self):
        for conn in self.base.sync_connections:
            a = Networking.receive(conn.sock)
            if a is None:
                self.base.sync_connections.remove(conn)

    def update_routines(self, routine: Routines):
        for rout in self.base.routines:
            if rout.name == "":
                self.base.routines.remove(rout)

            if rout.name == routine.name:
                self.base.routines.remove(rout)
                self.base.routines.append(routine)
