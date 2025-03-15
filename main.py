import sqlite3
import sys
from converters.convert import convert_data
from invoices.creator import generate_invoices
from migration import create_tables

conn = sqlite3.connect("network.db", detect_types=sqlite3.PARSE_DECLTYPES)

for x in sys.argv:
    if x == "createDatabase":
        print("Creating database")
        create_tables(conn)
    elif x == "loadData":
        convert_data(conn)
    elif x == "generateInvoice":
        generate_invoices(conn, "01.2025")