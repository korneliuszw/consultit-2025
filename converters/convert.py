from converters.customers import CustomerConverter
from converters.network_infrastructure import NetworkInfrastructureConverter
from converters.telemetry import TelemetryConverter
from database import DbSession


def convert_data(
    converters=[NetworkInfrastructureConverter, CustomerConverter, TelemetryConverter],
):
    with DbSession() as session:
        for converter in converters:
            print(f"Converting {converter.__name__}")
            conv = converter()
            conv.load_data()
            conv.to_database(session)
            print("Convert done")
        print("Converted everything")
