from os import environ

from converters.base import DataConverter

class NetworkInfrastructureConverter(DataConverter):
    def __init__(self):
        super().__init__(environ.get("NETWORK_INFRASTRUCTURE_DATA", "./data/infrastructure.csv"))

    def get_query(self):
        return """
            INSERT INTO NETWORK_INFRASTRUCTURE
                (ACCESS_POINT_ID, NAME, PARENT_ACCESS_POINT_ID, DEVICE_ORDER)
                VALUES (?, ?, ?, ?)
        """
    def get_device_order(row):
        id = row["ACCESS_POINT_ID"]
        if id[0] == "H":
            return 1
        elif id[0] == "R":
            return 2
        elif id == "IBAP":
            return 3
        else:
            return 0
    def to_tuple(self, row):
        return (row["ACCESS_POINT_ID"], row["NAME"], row["PARENT_ACCESS_POINT_ID"], NetworkInfrastructureConverter.get_device_order(row))

    