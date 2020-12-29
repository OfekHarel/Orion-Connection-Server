
class DataBase:
    """
    A structure that contains all the data of the server - a list of each type of connection.
    """
    def __init__(self):
        self.sync_connections = []
        self.connections = []

    def add(self, sync_connection=None, bridge_connection=None):
        """
        This function adds a connection to the connection's type list.
        """
        if sync_connection is not None:
            self.sync_connections.append(sync_connection)
        elif bridge_connection is not None:
            self.connections.append(bridge_connection)
        else:
            pass

    def remove(self, sync_connection=None, bridge_connection=None):
        """
        This function removes a connection to the connection's type list.
        """
        if sync_connection is not None:
            self.sync_connections.remove(sync_connection)
        elif bridge_connection is None:
            self.connections.remove(bridge_connection)
        else:
            pass

    def __str__(self):
        """
        A full description of the database's data
        """
        s = "Sync-> "
        for c in self.sync_connections:
            s += c.__str__() + " | "

        s += "\nConnections-> "
        for c in self.connections:
            s += c.__str__() + " | "

        return s
