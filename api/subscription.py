from typing import Annotated

from fastapi import APIRouter, Depends

from api.auth import ConsultantRequired
from api.pagination import PaginationResponseSchema, PaginationParams, paginate
from api.schemas.subscription import SubscriptionSchema
from database import SessionDep
from models import SubscriptionModel

router = APIRouter(
    prefix="/subscription",
    tags=["subscriptions"],
)


@router.get("/", response_model=PaginationResponseSchema[SubscriptionSchema])
def get_subscriptions(
    _: ConsultantRequired,
    params: Annotated[PaginationParams, Depends()],
    session: SessionDep,
):
    return paginate(session.query(SubscriptionModel), params, SubscriptionSchema)
