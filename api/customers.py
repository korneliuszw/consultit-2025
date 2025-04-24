from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from api.auth import ConsultantRequired
from api.pagination import PaginationParams, paginate, PaginationResponseSchema
from api.schemas.customers import (
    CustomerResponseSchema,
    CustomerUpdateSubscriptionPlan,
    CustomerAddBonusSchema,
)
from database import SessionDep
from models import CustomerModel, SubscriptionModel

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)


@router.get("/", response_model=PaginationResponseSchema[CustomerResponseSchema])
def get_customers(
    _: ConsultantRequired,
    session: SessionDep,
    params: Annotated[PaginationParams, Depends()],
):
    return paginate(session.query(CustomerModel), params, CustomerResponseSchema)


@router.post(
    "/subscription",
    response_model=CustomerResponseSchema,
    tags=["customers", "subscriptions"],
)
def set_customer_subscription_plan(
    _: ConsultantRequired, session: SessionDep, data: CustomerUpdateSubscriptionPlan
):
    customer = session.get(CustomerModel, data.customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    subscription = session.get(SubscriptionModel, data.plan_id)
    if subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    customer.subscription_plan_id = subscription.plan_id
    session.commit()
    return CustomerResponseSchema.model_validate(customer)


@router.post("/bonus", response_model=CustomerResponseSchema)
def give_bonus(
    _: ConsultantRequired, session: SessionDep, data: CustomerAddBonusSchema
):
    customer = session.get(CustomerModel, data.customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.marketing_bonus = data.marketing_bonus
    customer.einvoice_bonus = data.einvoice_bonus
    session.commit()
    return CustomerResponseSchema.model_validate(customer)
