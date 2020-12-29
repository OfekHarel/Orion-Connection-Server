from data_base.DataBase import DataBase
from utils.Enum import Enum


class Devices(Enum):
    APP = "APP"
    COMPUTER = "COMPUTER"


class DataTools:

    def __init__(self, base: DataBase):
        self.base = base

    def is_id_valid(self, device: Devices, id_num: str):
        for c in self.base.sync_connections:
            if c.id == id_num:
                return device == Devices.APP
        return device == Devices.COMPUTER

    def find(self, id_num: str):
        for c in self.base.sync_connections:
            if c.id == id_num:
                return c

        return None
