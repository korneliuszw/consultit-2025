from invoices.downtime_calculator import calculate_customer_downtime
from models import CustomerModel


def test_downtimes_calculator_overlapping_downtimes(seed_database):
    customer = seed_database.get(CustomerModel, "C2140")
    result = calculate_customer_downtime(seed_database, customer, "01.2025")
    assert result == 4


def test_downtimes_calculator_no_overlapping(seed_database):
    customer = seed_database.get(CustomerModel, "C2139")
    result = calculate_customer_downtime(seed_database, customer, "01.2025")
    assert result == 4


def test_downtimes_calculator_no_downtimes(seed_database):
    customer = seed_database.get(CustomerModel, "C2138")
    result = calculate_customer_downtime(seed_database, customer, "01.2025")
    assert result == 0
