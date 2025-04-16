from dataclasses import dataclass
from typing import List, Annotated

from fastapi import APIRouter, Depends

from api.auth import ServicemanRequired
from api.pagination import PaginationResponseSchema, PaginationParams, paginate
from api.schemas.downtimes import AccessPointResponseSchema
from database import SessionDep
from models import AccessPointModel

router = APIRouter(
    prefix="/infrastructure",
    tags=["infrastructure"],
)


@dataclass
class OrderMapping:
    device_type: str
    order: int


@router.get("/ordering")
def get_order_mapping(_: ServicemanRequired) -> List[OrderMapping]:
    return [
        OrderMapping(device_type="End-user", order=0),
        OrderMapping(device_type="Hub", order=1),
        OrderMapping(device_type="Router", order=2),
        OrderMapping(device_type="Provider", order=3),
    ]


@router.get("/", response_model=PaginationResponseSchema[AccessPointResponseSchema])
def get_infrastructure(
    _: ServicemanRequired,
    session: SessionDep,
    params: Annotated[PaginationParams, Depends()],
):
    return paginate(
        session.query(AccessPointModel).order_by(AccessPointModel.device_order.desc()),
        params,
        AccessPointResponseSchema,
    )
