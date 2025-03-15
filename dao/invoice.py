from enum import Enum
from sqlite3 import Connection, Cursor
from typing import List

class InvoiceLineTitle(Enum):
    SUBSCRIPTION = "SUBSCRIPTION"
    REBATE = "REBATE"
class InvoiceModel:
    id: int = None
    customer_id: str
    customer_name: str
    lines: int = 0

    def __init__(self, customer_id, customer_name, id = None):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.id = id
        pass

class InvoiceLineModel:
    invoice: InvoiceModel
    line_number: int
    title: InvoiceLineTitle
    amount: int

    def __init__(self, invoice: InvoiceModel, line_number: int, title: InvoiceLineTitle, amount: int):
        self.amount = amount
        self.invoice = invoice
        self.title = title
        self.line_number = line_number

class InvoiceDAO:
    def create(cursor: Cursor, data: InvoiceModel):
        """This will NOT commit to connection!"""
        cursor.execute("""
            INSERT INTO INVOICES(CUSTOMER_ID, CUSTOMER_NAME) VALUES (?, ?)
        """, (data.customer_id, data.customer_name))
        data.id = cursor.lastrowid

    def insert_line(cursor: Cursor, line: InvoiceLineModel):
        cursor.execute("""
            INSERT INTO INVOICE_LINES(INVOICE_ID, LINE_NUMBER, TITLE, LINE_AMOUNT) VALUES (?, ?, ?, ?)
        """, (line.invoice.id, line.line_number, line.title.value, line.amount))

    def get_all(conn: Connection) -> List[InvoiceModel]:
        result = conn.cursor().execute("""
            SELECT INVOICE_ID, CUSTOMER_ID, CUSTOMER_NAME
            FROM INVOICES
        """).fetchall()
        return [InvoiceModel(cid, cname, id) for id, cid, cname in result]
    
    def get_lines(conn: Connection, invoice: InvoiceModel) -> List[InvoiceLineModel]:
        result = conn.cursor().execute("""
            SELECT LINE_NUMBER, TITLE, LINE_AMOUNT
            FROM INVOICE_LINES
            WHERE INVOICE_ID = ?
        """, (str(invoice.id))).fetchall()
        return [InvoiceLineModel(invoice, line, title, amount) for line, title, amount in result]
