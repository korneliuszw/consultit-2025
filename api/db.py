import sqlite3

# TODO: Replace with async driver (chooooore)
conn = sqlite3.connect("network.db", detect_types=sqlite3.PARSE_DECLTYPES)
