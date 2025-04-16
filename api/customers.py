from typing import Annotated

from fastapi import APIRouter, Depends

from api.auth import ConsultantRequired
from api.pagination import PaginationParams, paginate, PaginationResponseSchema
from api.schemas.customers import CustomerResponseSchema
from database import SessionDep
from models import CustomerModel

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
