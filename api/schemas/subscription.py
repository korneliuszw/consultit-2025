from pydantic import BaseModel, ConfigDict, field_validator


class SubscriptionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    base_price: float
    final_price_formula: str

    @field_validator("base_price", mode="before")
    def convert_base_price(cls, value):
        """
        Convert base price from integer (grosze) to float (PLN)
        """
        if isinstance(value, int):
            return value / 100
        return value
