from invoices.creator import generate_single_invoice
from models import SubscriptionModel, CustomerModel, InvoiceLineModel


def test_invoice_generate_simple_plan_with_base_price_only(seed_database):
    # Setup simple subscription for user C2137
    simple_sub = SubscriptionModel(
        name="Simple", base_price=1000, final_price_formula="BASE_PRICE"
    )
    seed_database.add(simple_sub)
    customer = seed_database.get(CustomerModel, "C2137")
    customer.subscription = simple_sub
    seed_database.commit()
    # Test
    invoice = generate_single_invoice(seed_database, "01.2025", customer)
    assert invoice.subscription_used_formula == simple_sub.final_price_formula
    assert invoice.lines[0].title == "BASE_PRICE"
    assert invoice.lines[0].amount == 1000
    assert invoice.lines[1].title == "TOTAL_PRICE"
    assert invoice.lines[1].amount == 1000


def test_invoice_generate_formula_with_downtimes(seed_database):
    customer = seed_database.get(CustomerModel, "C2140")
    customer.owned_ip_addresses = 0
    seed_database.commit()
    invoice = generate_single_invoice(seed_database, "01.2025", customer)
    assert (
        seed_database.query(InvoiceLineModel)
        .filter(
            invoice.id == InvoiceLineModel.invoice_id,
            InvoiceLineModel.title == "DOWNTIME_DAYS",
        )
        .one()
        .amount
        == 4
    )
    assert (
        seed_database.query(InvoiceLineModel)
        .filter(
            invoice.id == InvoiceLineModel.invoice_id,
            InvoiceLineModel.title == "TOTAL_PRICE",
        )
        .one()
        .amount
    ) == 7336


def test_invoice_generate_formula_with_all_variables(seed_database):
    customer = seed_database.get(CustomerModel, "C2140")
    customer.owned_ip_addresses = 4
    customer.marketing_bonus = True
    customer.einvoice_bonus = True
    customer.subscription_plan_id = 3
    seed_database.commit()
    invoice = generate_single_invoice(seed_database, "01.2025", customer)
    assert (
        seed_database.query(InvoiceLineModel)
        .filter(
            invoice.id == InvoiceLineModel.invoice_id,
            InvoiceLineModel.title == "TOTAL_PRICE",
        )
        .one()
        .amount
        == 7836
    )
