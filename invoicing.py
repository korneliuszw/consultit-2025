from datetime import date, timedelta
from math import floor
from sqlite3 import Connection

from dao.access_points import AccessPointDAO, AccessPointModel
from dao.customers import CustomerDAO, CustomerModel
from dao.invoice import InvoiceDAO, InvoiceLineModel, InvoiceLineTitle, InvoiceModel
from dao.telemetry import TelemetryLogDAO, TelemetryLogModel

def create_device_lookup_table(devices: AccessPointModel) -> dict[str, set[str]]:
    """This assumes devices are sorted by their device order!"""
    """Builds a map of connections between device and customer devices"""
    lookup_table: dict[str, set[str]] = {}
    for device in devices:
        if device.parent is None or device.parent == "": continue
        if device.id[0] == "D":
            lookup_table[device.id] = set()
            lookup_table[device.id].add(device.id) # self cycle for less conditions
        if device.parent not in lookup_table:
            lookup_table[device.parent] = set()
        lookup_table[device.parent].update(lookup_table[device.id])
    return lookup_table

ProcessedDowntimeType = list[tuple[str, list[date]]]

def preprocess_downtime(downtime: TelemetryLogModel) -> ProcessedDowntimeType:
    start = downtime.start_date.date()
    month = start.month
    end = downtime.end_date.date()
    dates = []
    while True:
        if start.month != month or start > end:
            break;
        dates.append(start)
        start += timedelta(days=1)
    return (downtime.access_point_id, dates)

def process_downtimes(downtimes: ProcessedDowntimeType, devices: list[AccessPointModel]):
    """Turn all preprocesed downtimes into downtimes only for end-client nodes"""
    device_lookup = create_device_lookup_table(devices)
    client_device_downtimes: dict[str, set[date]] = {}
    for id, dates in downtimes:
        for client in device_lookup[id]:
            if client not in client_device_downtimes:
                client_device_downtimes[client] = set() # Use set so we don't bill many times for many outages on the same day
            client_device_downtimes[client].update(set(dates))
    return client_device_downtimes

def load_client_downtimes_for_month(conn: Connection, month):
    devices = AccessPointDAO.get_all(conn)
    downtimes = list(map(lambda x: preprocess_downtime(x), TelemetryLogDAO.get_in_month(conn, month)))
    return process_downtimes(downtimes, devices)

def generate_invoices(conn: Connection, month):
    client_device_downtimes = load_client_downtimes_for_month(conn, month)
    customers: list[CustomerModel] = CustomerDAO.get_all(conn)
    for customer in customers:
        invoice = InvoiceModel(customer.id, customer.name)
        invoice_lines: set[InvoiceLineModel] = [InvoiceLineModel(invoice, 0, InvoiceLineTitle.SUBSCRIPTION, customer.monthly_amount_due)]
        affected_downtimes = client_device_downtimes[customer.access_point]
        if len(affected_downtimes) > 0:
            downtime_rebate = len(affected_downtimes) * floor(customer.monthly_amount_due / 30) # We store as cents so discard more than that
            invoice_lines.append(InvoiceLineModel(invoice, 1, InvoiceLineTitle.REBATE, -downtime_rebate))
        cursor = conn.cursor()
        InvoiceDAO.create(cursor, invoice)
        for line in invoice_lines:
            InvoiceDAO.insert_line(cursor, line)
        conn.commit()