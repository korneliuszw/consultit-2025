from pydantic import BaseModel, ConfigDict


class CustomerResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    monthly_amount_due: int
