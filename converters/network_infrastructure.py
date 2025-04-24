from os import environ

from converters.base import DataConverter
from models import AccessPointModel


class NetworkInfrastructureConverter(DataConverter[AccessPointModel]):
    def to_model(self, row) -> AccessPointModel:
        return AccessPointModel(
            id=row["ACCESS_POINT_ID"],
            name=row["NAME"],
            parent_access_point_id=row["PARENT_ACCESS_POINT_ID"],
            device_order=NetworkInfrastructureConverter.get_device_order(row),
        )

    def __init__(self):
        super().__init__(
            environ.get("NETWORK_INFRASTRUCTURE_DATA", "./data/infrastructure.csv")
        )

    @staticmethod
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
