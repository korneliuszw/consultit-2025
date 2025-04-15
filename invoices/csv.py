import os
from os import environ, mkdir, path
from typing import List

from sqlalchemy.orm import Session

import csv
from database import DbSession
from models import InvoiceModel, InvoiceLineModel
from repository import InvoiceRepository

out_dir = environ.get("INVOICE_CSV_OUT_DIR", path.join(os.getcwd(), "output"))


def ensure_dir(dir):
    if path.isfile(dir):
        raise Exception(f"Directory {dir} is a file not a directory")
    elif not path.exists(dir):
        print(f"Directory {dir} doesn't exist. Creating it now")
        mkdir(dir)


ensure_dir(out_dir)


def get_invoice_name(invoice: InvoiceModel):
    return f"invoice_{invoice.id}_{invoice.customer_id}_{invoice.month}"


def create_single_csv(session: Session, invoice: InvoiceModel):
    out_path = path.join(out_dir, f"{get_invoice_name(invoice)}.csv")
    lines: List[InvoiceLineModel] = InvoiceRepository.get_lines(invoice)
    if len(lines) == 0:
        return
    with open(out_path, "w+", newline="") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(["INVOICE_ID", "CUSTOMER_ID", "CUSTOMER_NAME"])
        writer.writerow([invoice.id, invoice.customer_id, invoice.customer_name])
        writer.writerow(["LINE_NUMBER", "TITLE", "LINE_AMOUNT"])
        for line in lines:
            writer.writerow([line.line_number, line.title, line.amount / 100])


def generate_invoices_for_all(month=None):
    with DbSession() as session:
        invoices: List[InvoiceModel] = (
            InvoiceRepository.get_all(session)
            if month is None
            else InvoiceRepository.get_for_month(session, month)
        )
        for invoice in invoices:
            create_single_csv(session, invoice)
