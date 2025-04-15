from os import environ

from converters.base import DataConverter
from models import CustomerModel


class CustomerConverter(DataConverter[CustomerModel]):
    def to_model(self, row) -> CustomerModel:
        return CustomerModel(
            id=row["ID"],
            name=row["NAME"],
            access_point=row["ACCESS_POINT"],
            monthly_amount_due=int(row["MONTHLY_AMOUNT_DUE"]) * 100,
        )

    def __init__(self):
        super().__init__(environ.get("CUSTOMERS_DATA", "./data/customers.csv"))
