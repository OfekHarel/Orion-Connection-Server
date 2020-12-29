
class DataBase:
    def __init__(self):
        self.sync_connections = []
        self.connections = []
        self.ids = []

    def add(self, sync_connection=None, bridge_connection=None):
        if sync_connection is not None:
            self.sync_connections.append(sync_connection)
        elif bridge_connection is not None:
            self.connections.append(bridge_connection)
        else:
            pass

    def remove(self, sync_connection=None, bridge_connection=None):
        if sync_connection is not None:
            self.sync_connections.remove(sync_connection)
        elif bridge_connection is None:
            self.connections.remove(bridge_connection)
        else:
            pass

    def __str__(self):
        s = "Sync-> "
        for c in self.sync_connections:
            s += c.__str__() + " | "

        s += "\nConnections-> "
        for c in self.connections:
            s += c.__str__() + " | "

        return s
