from sqlite3 import Connection
from converters.customers import CustomerConverter
from converters.network_infrastructure import NetworkInfrastructureConverter
from converters.telemetry import TelemetryConverter

def convert_network_infrastucture(conn: Connection):
    print("Converting network infrastructure")
    conv = NetworkInfrastructureConverter()
    conv.load_data()
    conv.to_database(conn)
    print("Convert done")


def convert_data(conn: Connection, converters=[NetworkInfrastructureConverter, CustomerConverter, TelemetryConverter]):
    for converter in converters:
        print(f"Converting {converter.__name__}")
        conv = converter()
        conv.load_data()
        conv.to_database(conn)
        print("Convert done")
    print("Converted everything")