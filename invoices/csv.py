import csv
from os import environ, mkdir, path
import os
from sqlite3 import Connection
from typing import List
from dao.invoice import InvoiceDAO, InvoiceLineModel, InvoiceModel

out_dir = environ.get("INVOICE_CSV_OUT_DIR", path.join(os.getcwd(), "output"))

if path.isfile(out_dir):
    raise Exception("Output directory is a file not a directory")
elif not path.exists(out_dir):
    print("Output directory doesn't exist. Creating it now")
    mkdir(out_dir)

def get_invoice_name(invoice: InvoiceModel):
    return f"invoice_{invoice.id}_{invoice.customer_id}"

def create_single_csv(conn: Connection, invoice: InvoiceModel):
    out_path = path.join(out_dir, f"{get_invoice_name(invoice)}.csv")
    lines: List[InvoiceLineModel] = InvoiceDAO.get_lines(conn, invoice)
    if len(lines) == 0: return
    with open(out_path, "w+", newline='') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(["INVOICE_ID", "CUSTOMER_ID", "CUSTOMER_NAME"])
        writer.writerow([invoice.id, invoice.customer_id, invoice.customer_name])
        writer.writerow(["LINE_NUMBER", "TITLE", "LINE_AMOUNT"])
        for line in lines:
            writer.writerow([line.line_number, line.title, line.amount / 100])

def generate_invoices_for_all(conn: Connection):
    invoices: List[InvoiceModel] = InvoiceDAO.get_all(conn)
    for invoice in invoices:
        create_single_csv(conn, invoice)
