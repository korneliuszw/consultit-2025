from typing import List, Type

from sqlalchemy.orm import Session

from database import DbSession
from invoices.formula import FormulaEval
from models import (
    CustomerModel,
    InvoiceModel,
    InvoiceLineModel,
)
from repository import (
    CustomerRepository,
    InvoiceRepository,
)

DeviceLookupType = dict[str, set[str]]


def generate_invoices(month):
    with DbSession() as session:
        customers: List[Type[CustomerModel]] = CustomerRepository.get_all(session)
        for customer in customers:
            generate_single_invoice(session, month, customer)


def generate_single_invoice(session: Session, month, customer: CustomerModel):
    subscription = customer.subscription
    formula_evaluator = FormulaEval(
        customer=customer, subscription=subscription, month=month
    )
    total = formula_evaluator.eval(subscription.final_price_formula)
    invoice = InvoiceModel(
        customer_id=customer.id,
        customer_name=customer.name,
        month=month,
        subscription_plan_name=subscription.name,
        subscription_used_formula=subscription.final_price_formula,
    )
    lines = []
    variables = formula_evaluator.get_used_variables()
    variables.append(("TOTAL_PRICE", total))
    for index, variable in enumerate(variables):
        title, amount = variable
        amount = int(amount)
        lines.append(
            InvoiceLineModel(
                invoice=invoice, title=title, amount=amount, line_number=index + 1
            )
        )
    InvoiceRepository.create(session, invoice)
    InvoiceRepository.insert_lines(session, lines)
    session.commit()
    return invoice
