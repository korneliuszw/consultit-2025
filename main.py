from datetime import datetime
import sqlite3
import sys
from converters.convert import convert_data
from invoices.creator import generate_invoices
from invoices.csv import generate_invoices_for_all
from invoices.pdf import generate_pdf_invoices_for_all
from migration import create_tables

conn = sqlite3.connect("network.db", detect_types=sqlite3.PARSE_DECLTYPES)

def get_month_from_cli(cur_idx, optional=False):
    try:
        if len(sys.argv) <= cur_idx + 1: raise Exception("Missing month argument")
        str_arg = sys.argv[cur_idx + 1]
        datetime.strptime(str_arg, "%m.%Y")
        return str_arg
    except Exception as e:
        if (optional):
            return None
        raise e

for idx, x in enumerate(sys.argv):
    if x == "createDatabase":
        print("Creating database")
        create_tables(conn)
    elif x == "loadData":
        convert_data(conn)
    elif x == "generateInvoice":
        generate_invoices(conn, get_month_from_cli(idx))
    elif x == "invoicesToCSV":
        generate_invoices_for_all(conn, get_month_from_cli(idx, True))
    elif x == "invoicesToPdf":
        generate_pdf_invoices_for_all(conn, get_month_from_cli(idx, True))