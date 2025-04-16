from datetime import datetime
from os import environ, mkdir, path, getcwd
from typing import List

from mako.template import Template
from sqlalchemy.orm import Session
from weasyprint import HTML

from database import DbSession
from invoices.csv import get_invoice_name
from models import InvoiceModel, InvoiceLineModel
from repository import InvoiceRepository

out_dir = environ.get("INVOICE_CSV_OUT_DIR", path.join(getcwd(), "output"))

template_path = environ.get("INVOICE_HTML_TEMPLATE", "./invoices/template.html")
template = Template(filename=template_path)

if path.isfile(out_dir):
    raise Exception("Output directory is a file not a directory")
elif not path.exists(out_dir):
    print("Output directory doesn't exist. Creating it now")
    mkdir(out_dir)


def create_single_pdf(session: Session, invoice: InvoiceModel):
    out_path = path.join(out_dir, f"{get_invoice_name(invoice)}.pdf")
    items: List[InvoiceLineModel] = InvoiceRepository.get_lines(invoice)
    creation_date = str(datetime.now().date())
    customer_address = "ul. Wyspiańskiego 5A"
    customer_city = "80-434 Gdańsk"
    total = sum([line.amount for line in items])
    html = template.render(
        total=total,
        customer_name=invoice.customer_name,
        customer_address=customer_address,
        customer_city=customer_city,
        items=items,
        creation_date=creation_date,
        invoice_id=invoice.id,
        month=invoice.month,
    )
    HTML(string=html).write_pdf(out_path)
    return out_path


def generate_pdf_invoices_for_all(month: str):
    with DbSession() as session:
        invoices: List[InvoiceModel] = (
            InvoiceRepository.get_all(session)
            if month is None
            else InvoiceRepository.get_for_month(session, month)
        )
        for invoice in invoices:
            create_single_pdf(session, invoice)
