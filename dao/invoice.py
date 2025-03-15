from enum import Enum
from sqlite3 import Cursor

class InvoiceLineTitle(Enum):
    SUBSCRIPTION = "SUBSCRIPTION"
    REBATE = "REBATE"


class InvoiceModel:
    id: int = None
    customer_id: str
    customer_name: str
    lines: int = 0

    def __init__(self, customer_id, customer_name):
        self.customer_id = customer_id
        self.customer_name = customer_name
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



