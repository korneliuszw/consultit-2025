import sqlite3
import sys
from converters.convert import convert_data
from migration import create_tables

conn = sqlite3.connect("network.db")

for x in sys.argv:
    if x == "createDatabase":
        print("Creating database")
        create_tables(conn)
    elif x == "loadData":
        convert_data(conn)
        