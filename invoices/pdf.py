from datetime import datetime
from os import environ, mkdir, path, getcwd
from sqlite3 import Connection
from typing import List
from mako.template import Template
from weasyprint import HTML

from dao.invoice import InvoiceDAO, InvoiceLineModel, InvoiceModel
from invoices.csv import get_invoice_name

out_dir = environ.get("INVOICE_CSV_OUT_DIR", path.join(getcwd(), "output"))

template_path = environ.get("INVOICE_HTML_TEMPLATE", "./invoices/template.html")
template = Template(filename=template_path)

if path.isfile(out_dir):
    raise Exception("Output directory is a file not a directory")
elif not path.exists(out_dir):
    print("Output directory doesn't exist. Creating it now")
    mkdir(out_dir)

def create_single_pdf(conn: Connection, invoice: InvoiceModel):
    out_path = path.join(out_dir, f"{get_invoice_name(invoice)}.pdf")
    items: List[InvoiceLineModel] = InvoiceDAO.get_lines(conn, invoice)
    creation_date = str(datetime.now().date())
    customer_address = "ul. Wyspiańskiego 5A"
    customer_city = "80-434 Gdańsk"
    total = sum([line.amount for line in items])
    html = template.render(total=total,
                        customer_name=invoice.customer_name,
                        customer_address=customer_address,
                        customer_city=customer_city,
                        items=items,
                        creation_date=creation_date,
                        invoice_id=invoice.id,
                        month=invoice.month
                        )
    HTML(string=html).write_pdf(out_path)

def generate_pdf_invoices_for_all(conn: Connection, month: str):
    invoices: List[InvoiceModel] = InvoiceDAO.get_all(conn) if month is None else InvoiceDAO.get_for_month(conn, month)
    for invoice in invoices:
        create_single_pdf(conn, invoice)

