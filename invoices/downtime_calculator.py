from datetime import date, timedelta
from typing import List, Type

from sqlalchemy.orm import Session

from models import (
    TelemetryLogModel,
    CustomerModel,
)
from repository import (
    TelemetryLogRepository,
)

DeviceLookupType = dict[str, set[str]]


def create_single_customer_device_lookup_table(
    customer: Type[CustomerModel],
) -> DeviceLookupType:
    lookup_table: dict[str, set[str]] = {}
    device = customer.device
    affected_devices = []
    while device is not None:
        lookup_table[device.id] = set()
        lookup_table[device.id].add(customer.access_point)
        affected_devices.append(device.id)
        device = device.parent
    return lookup_table, affected_devices


ProcessedDowntimeType = tuple[str, List[date]]


def preprocess_downtime(downtime: TelemetryLogModel) -> ProcessedDowntimeType:
    start = downtime.start_date.date()
    month = start.month
    end = downtime.end_date.date()
    dates = []
    while True:
        if start.month != month or start > end:
            break
        dates.append(start)
        start += timedelta(days=1)
    return downtime.access_point_id, dates


def process_downtimes(
    downtimes: List[ProcessedDowntimeType],
    device_lookup: DeviceLookupType,
):
    """Turn all preprocesed downtimes into downtimes only for end-client nodes"""
    client_device_downtimes: dict[str, set[date]] = {}
    for id, dates in downtimes:
        for client in device_lookup[id]:
            if client not in client_device_downtimes:
                client_device_downtimes[client] = (
                    set()
                )  # Use set so we don't bill many times for many outages on the same day
            client_device_downtimes[client].update(set(dates))
    return client_device_downtimes


def load_client_downtimes_for_month(
    session: Session, month, device_lookup: DeviceLookupType, affected_devices=None
):
    downtimes = list(
        map(
            lambda x: preprocess_downtime(x),
            TelemetryLogRepository.get_in_month(session, month, affected_devices),
        )
    )
    print(TelemetryLogRepository.get_in_month(session, month))
    return process_downtimes(downtimes, device_lookup)


def calculate_customer_downtime(session: Session, customer: CustomerModel, month: str):
    device_lookup, affected_devices = create_single_customer_device_lookup_table(
        customer
    )
    client_device_downtimes = load_client_downtimes_for_month(
        session, month, device_lookup, affected_devices
    )
    return len(client_device_downtimes.get(customer.access_point, []))
