from sqlite3 import Connection
from typing import List


class CustomerModel:
    id: str
    name: str
    access_point: str
    monthly_amount_due: int

    def __init__(self, id, name, access_point, monthly_amount_due):
        self.access_point = access_point
        self.id = id
        self.name = name
        self.monthly_amount_due = monthly_amount_due

class CustomerDAO:
    def get_all(conn: Connection) -> List[CustomerModel]:
        result = conn.cursor().execute("""
           SELECT ID, NAME, ACCESS_POINT, MONTHLY_AMOUNT_DUE
            FROM CUSTOMERS
        """).fetchall()
        return list(map(lambda value: CustomerModel(value[0], value[1], value[2], value[3]), result))