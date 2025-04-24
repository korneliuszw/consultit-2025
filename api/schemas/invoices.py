import re
from typing import List

from pydantic import BaseModel, ConfigDict, field_validator


class InvoiceLineResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    amount: int


class InvoiceResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    customer_id: str
    customer_name: str
    month: str
    lines: List[InvoiceLineResponseSchema]


class InvoiceCreateSchema(BaseModel):
    customer_id: str
    month: str

    @field_validator("month")
    def validate_month_format(cls, value):
        # Define the required format regex for MM.YYYY
        if not re.match(r"^(0[1-9]|1[0-2])\.\d{4}$", value):
            raise ValueError("Invalid format for month. Expected format is 'MM.YYYY'.")
        return value
