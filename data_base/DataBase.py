class DataBase:
    """
    A structure that contains all the data of the server - a list of each type of connection.
    """
    def __init__(self):
        self.sync_connections = []
        self.connections = []

    def add(self, bridge=None, sync=None):
        """
        This function adds a connection to the connection's type list.
        """
        if bridge is not None:
            self.connections.append(bridge)

        elif sync is not None:
            self.sync_connections.append(sync)

        else:
            pass

    def remove(self, bridge=None, sync=None, routine_name=None):
        """
        This function removes a connection to the connection's type list.
        """
        if bridge is not None:
            self.connections.remove(bridge)

        elif sync is not None:
            self.sync_connections.remove(sync)

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
            s += c.__str__()

        return s
