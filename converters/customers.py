from os import environ

from converters.base import DataConverter

class CustomerConverter(DataConverter):
    def __init__(self):
        super().__init__(environ.get("CUSTOMERS_DATA", "./data/customers.csv"))

    def get_query(self):
        return """
            INSERT INTO CUSTOMERS 
                (ID, NAME, ACCESS_POINT, MONTHLY_AMOUNT_DUE)
                VALUES (?, ?, ?, ?)
        """

    def to_tuple(self, row):
        return (row["ID"], row["NAME"], row["ACCESS_POINT"], int(row["MONTHLY_AMOUNT_DUE"]) * 100)

    