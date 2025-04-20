from pydantic import BaseModel, ConfigDict

from api.schemas.subscription import SubscriptionSchema


class CustomerResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    owned_ip_addresses: int
    marketing_bonus: bool
    einvoice_bonus: bool
    subscription: SubscriptionSchema


class CustomerUpdateSubscriptionPlan(BaseModel):
    customer_id: str
    plan_id: int


class CustomerAddBonusSchema(BaseModel):
    customer_id: str
    einvoice_bonus: bool
    marketing_bonus: bool
