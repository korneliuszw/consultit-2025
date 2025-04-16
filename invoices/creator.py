from datetime import date, timedelta
from math import floor
from typing import List, Type

from sqlalchemy.orm import Session

from database import DbSession
from models import (
    TelemetryLogModel,
    CustomerModel,
    InvoiceModel,
    InvoiceLineModel,
    InvoiceLineTitle,
)
from repository import (
    AccessPointRepository,
    TelemetryLogRepository,
    CustomerRepository,
    InvoiceRepository,
)

DeviceLookupType = dict[str, set[str]]


def create_device_lookup_table(session: Session) -> DeviceLookupType:
    """This assumes devices are sorted by their device order!"""
    """Builds a map of connections between device and customer devices"""
    """Faster for genering invoices for all customers, slower for only one (less database queries but more calculations)"""
    devices = AccessPointRepository.get_all(session)
    lookup_table: dict[str, set[str]] = {}
    for device in devices:
        if device.parent_access_point_id is None or device.parent_access_point_id == "":
            continue
        if device.id[0] == "D":
            lookup_table[device.id] = set()
            lookup_table[device.id].add(device.id)  # self cycle for less conditions
        print(f"Adding {device.id} to {device.parent_access_point_id}")
        if device.parent_access_point_id not in lookup_table:
            lookup_table[device.parent_access_point_id] = set()
        lookup_table[device.parent_access_point_id].update(lookup_table[device.id])
    return lookup_table


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
    return process_downtimes(downtimes, device_lookup)


def create_invoice(
    session: Session, month, customer: CustomerModel, client_device_downtimes
):
    invoice = InvoiceModel(
        customer_id=customer.id, customer_name=customer.name, month=month
    )
    invoice_lines: list[InvoiceLineModel] = [
        InvoiceLineModel(
            invoice=invoice,
            line_number=0,
            title=InvoiceLineTitle.SUBSCRIPTION,
            amount=customer.monthly_amount_due,
        )
    ]
    affected_downtimes = client_device_downtimes.get(customer.access_point, [])
    if len(affected_downtimes) > 0:
        downtime_rebate = len(affected_downtimes) * floor(
            customer.monthly_amount_due / 30
        )  # We store as cents so discard more than that
        invoice_lines.append(
            InvoiceLineModel(
                invoice=invoice,
                line_number=1,
                title=InvoiceLineTitle.REBATE,
                amount=-downtime_rebate,
            )
        )
    InvoiceRepository.create(session, invoice)
    InvoiceRepository.insert_lines(session, invoice_lines)
    session.commit()
    return invoice


def generate_invoices(month):
    with DbSession() as session:
        device_lookup = create_device_lookup_table(session)
        client_device_downtimes = load_client_downtimes_for_month(
            session, month, device_lookup
        )
        customers: List[Type[CustomerModel]] = CustomerRepository.get_all(session)
        for customer in customers:
            create_invoice(session, month, customer, client_device_downtimes)


def generate_single_invoice(session: Session, month, customer: Type[CustomerModel]):
    device_lookup, affected_devices = create_single_customer_device_lookup_table(
        customer
    )
    client_device_downtimes = load_client_downtimes_for_month(
        session, month, device_lookup, affected_devices
    )
    return create_invoice(session, month, customer, client_device_downtimes)
